import database
from admin.cmdparse import CommandParser

parser = CommandParser(alias={
    'hostname': '(?:\w+)',
    'username': '(?:\w+)',
    'new': '(?:add|new)',
    'delete': '(?:delete|del|remove|rm)',
    'grant': '(?:allow|grant|add)',
    'revoke': '(?:deny|revoke|remove|rm|delete|del)',
    'to': '(?:to|on)',
    'from': '(?:from|on)',
})


@parser.register("^new server (hostname)$")
def new_server(hostname):
    """create a new server by name"""
    return database.add_server(hostname)


@parser.register("^delete server (hostname)$")
def delete_server(hostname):
    """delete an existing server by name"""
    return database.remove_server(hostname)


@parser.register("^new user (username)$")
def new_user(username):
    """create a new user by name"""
    return database.add_user(username)


@parser.register("^delete user (username)$")
def delete_user(username):
    """delete an existing user by name"""
    return database.remove_user(username)


@parser.register("^grant (username) to (hostname)$")
def grant_access(username, hostname):
    """grant access to a user on an existing server"""
    return database.grant_access(username, hostname)


@parser.register("^revoke (username) from (hostname)$")
def revoke_access(username, hostname):
    """revoke access to a user from an existing server"""
    return database.revoke_access(username, hostname)


def parse(command):
    return parser.parse(command)


def help():
    return parser.help()
