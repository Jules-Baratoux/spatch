import shelve

from os import path


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


def create(table, name, value):
    call('__setitem__', table, "%r already exists" % name, False, name, value)


def delete(table, name):
    call('__delitem__', table, "%r does not exists" % name, True, name)


def get(table, name):
    return call('__getitem__', table, "%r does not exists" % name, True, name)


def update(table, name, value):
    call('__setitem__', table, "%r does not exists" % name, True, name, value)


def new_server(hostname):
    """ Add a server by hostname
    :param hostname: the server's hostname
    """
    create('servers', hostname, {})
    # print "new_server(%r)" % hostname


def delete_server(hostname):
    """ Remove a server by hostname
    :param hostname: the server's hostname
    """
    delete('servers', hostname)
    # print "delete_server(%r)" % hostname


def new_user(username):
    """ Add a user by name
    :param username: the user's name
    """
    create('users', username, {})
    # print "new_user(%r)" % username


def delete_user(username):
    """ Remove a user by name
    :param username: the user's name
    """
    delete('users', username)
    # print "delete_user(%r)" % username


def grant_access(username, hostname):
    """ Grant access to a user on a server
    :param username: the user's name
    :param hostname: the server's hostname
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    server = get('servers', hostname)
    server[username] = True
    update('servers', hostname, server)
    # print "grant_access(%r, %r)" % (username, hostname)


def revoke_access(username, hostname):
    """ Revoke access to a user on a server
    :param username: the user's name
    :param hostname: the server's hostname
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    server = get('servers', hostname)
    server[username] = False
    update('servers', hostname, server)
    # print "revoke_access(%r, %r)" % (username, hostname)


def access_granted(username, hostname):
    """ Returns whether a user has access to a server or not
    :param username: the user's name
    :param hostname: the server's hostname
    :return: True or False
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    server = get('servers', hostname)
    try:
        result = server[username] == True
    except KeyError:
        result = False
    # print "access_granted(%r,%r) -> %s" % (username, hostname, result)
    return result
