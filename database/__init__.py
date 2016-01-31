def add_server(hostname):
    """ Add a server by hostname
    :param hostname: the server's hostname
    """
    assert isinstance(hostname, str)
    raise NotImplementedError


def remove_server(hostname):
    """ Remove a server by hostname
    :param hostname: the server's hostname
    """
    assert isinstance(hostname, str)
    raise NotImplementedError


def add_user(username):
    """ Add a user by name
    :param username: the user's name
    """
    assert isinstance(username, str)
    raise NotImplementedError


def remove_user(username):
    """ Remove a user by name
    :param username: the user's name
    """
    assert isinstance(username, str)
    raise NotImplementedError


def grant_access(username, hostname):
    """ Grant access to a server
    :param username: the user's name
    :param hostname: the server's hostname
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    raise NotImplementedError


def revoke_access(username, hostname):
    """ Revoke access to a server
    :param username: the user's name
    :param hostname: the server's hostname
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    raise NotImplementedError


def access_granted(username, hostname):
    """ Returns whether a user has access to a server or not
    :param username: the user's name
    :param hostname: the server's hostname
    :return: True or False
    """
    assert isinstance(username, str)
    assert isinstance(hostname, str)
    # raise NotImplementedError
    return True
