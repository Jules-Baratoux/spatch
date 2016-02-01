def access_granted(username, hostname):
    """ Returns whether a user has access to a server or not
    :param username: the user's name
    :param hostname: the server's hostname
    :return: True or False
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    raise NotImplementedError("access_granted(%r,%r)" % (username, hostname))


def add_server(hostname):
    """ Add a server by hostname
    :param hostname: the server's hostname
    """
    assert isinstance(hostname, str)
    raise NotImplementedError("add_server(%r)" % (hostname))


def remove_server(hostname):
    """ Remove a server by hostname
    :param hostname: the server's hostname
    """
    assert isinstance(hostname, str)
    raise NotImplementedError("remove_server(%r)" % (hostname))


def add_user(username):
    """ Add a user by name
    :param username: the user's name
    """
    assert isinstance(username, str)
    raise NotImplementedError("add_user(%r)" % (username))


def remove_user(username):
    """ Remove a user by name
    :param username: the user's name
    """
    assert isinstance(username, str)
    raise NotImplementedError("remove_user(%r)" % (username))


def grant_access(username, hostname):
    """ Grant access to a user on a server
    :param username: the user's name
    :param hostname: the server's hostname
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    raise NotImplementedError("grant_access(%r, %r)" % (username, hostname))


def revoke_access(username, hostname):
    """ Revoke access to a user on a server
    :param username: the user's name
    :param hostname: the server's hostname
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    raise NotImplementedError("revoke_access(%r, %r)" % (username, hostname))