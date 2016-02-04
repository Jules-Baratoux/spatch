import shelve

from os import path

from splatchd.models import User

from splatchd.models import Server


class Cache(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __getitem__(self, name):
        shelf = shelve.open(*self.args, **self.kwargs)
        result = shelf.__getitem__(name)
        shelf.close()
        return result

    def __setitem__(self, name, value):
        shelf = shelve.open(*self.args, **self.kwargs)
        result = shelf.__setitem__(name, value)
        shelf.close()
        return result

    def __delitem__(self, name, value):
        shelf = shelve.open(*self.args, **self.kwargs)
        result = shelf.__delitem__(name)
        shelf.close()
        return result


filename = path.dirname(__file__) + '.db'
cache = Cache(filename, flag='c')


def call(method, table, message, contains, name, *args):
    try:
        tmp = cache[table]
    except KeyError:
        tmp = cache[table] = {}

    assert isinstance(name, str)
    assert (name in tmp) == contains, message
    result = getattr(tmp, method)(name, *args)
    cache[table] = tmp
    return result


def _create(table, name, value):
    call('__setitem__', table, "%r already exists" % name, False, name, value)


def _delete(table, name):
    call('__delitem__', table, "%r does not exists" % name, True, name)


def _get(table, name):
    return call('__getitem__', table, "%r does not exists" % name, True, name)


def _update(table, name, value):
    call('__setitem__', table, "%r does not exists" % name, True, name, value)


def new_server(hostname, port):
    """ Add a server by hostname
    :param hostname: the server's hostname
    """
    server = Server(hostname, port)
    _create('servers', hostname, server)
    # print "new_server(%r)" % hostname


def delete_server(hostname):
    """ Remove a server by hostname
    :param hostname: the server's hostname
    """
    _delete('servers', hostname)
    # print "delete_server(%r)" % hostname


def new_user(username, public_key_filename):
    """ Add a user by name
    :param username: the user's name
    """
    user = User(username, public_key_filename)
    _create('users', username, user)
    # print "new_user(%r)" % username


def delete_user(username):
    """ Remove a user by name
    :param username: the user's name
    """
    _delete('users', username)
    # print "delete_user(%r)" % username


def grant_access(username, hostname, alias):
    """ Grant access to a user on a server
    :param username: the user's name
    :param hostname: the server's hostname
    :param alias: the username used on the server
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    server = _get('servers', hostname)
    server.alias_by_username[username] = alias
    _update('servers', hostname, server)
    # print "grant_access(%r, %r)" % (username, hostname)


def revoke_access(username, hostname):
    """ Revoke access to a user on a server
    :param username: the user's name
    :param hostname: the server's hostname
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    server = _get('servers', hostname)
    server[username] = False
    _update('servers', hostname, server)
    # print "revoke_access(%r, %r)" % (username, hostname)


def access_granted(username, hostname):
    """ Returns whether a user has access to a server or not
    :param username: the user's name
    :param hostname: the server's hostname
    :return: str if granted else None
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    server = _get('servers', hostname)
    try:
        return server.alias_by_username[username]
    except KeyError:
        return None
    # print "access_granted(%r,%r) -> %s" % (username, hostname, result)
