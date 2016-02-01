import database
from admin import cmdparse

alias = {
    'hostname': '(?:\w+)',
    'username': '(?:\w+)',
    'new': '(?:add|new)',
    'delete': '(?:delete|del|remove|rm)',
    'grant': '(?:allow|grant|add)',
    'revoke': '(?:deny|revoke|remove|rm|delete|del)',
    'to': '(?:to|on)',
    'from': '(?:from|on)',
}


@cmdparse.register(pattern="^new server (hostname)$", alias=alias)
def new_server(match):
    """create a new server by name"""
    return database.add_server(*match.groups())


@cmdparse.register(pattern="^delete server (hostname)$", alias=alias)
def delete_server(match):
    """delete an existing server by name"""
    return database.remove_server(*match.groups())


@cmdparse.register(pattern="^new user (username)$", alias=alias)
def new_user(match):
    """create a new user by name"""
    return database.add_user(*match.groups())


@cmdparse.register(pattern="^delete user (username)$", alias=alias)
def delete_user(match):
    """delete an existing user by name"""
    return database.remove_user(*match.groups())


@cmdparse.register(pattern="^grant (username) to (hostname)$", alias=alias)
def grant_access(match):
    """grant access to a user on an existing server"""
    return database.grant_access(*match.groups())


@cmdparse.register(pattern="^revoke (username) from (hostname)$", alias=alias)
def revoke_access(match):
    """revoke access to a user from an existing server"""
    return database.revoke_access(*match.groups())


def parse(command):
    return cmdparse.process(command)


def help():
    return cmdparse.help()
