import database
from admin.cmdparse import CommandParser

commands = CommandParser(alias={
    'hostname': '(?:\w+)',
    'username': '(?:\w+)',
    'new':      '(?:add|new)',
    'delete':   '(?:delete|del|remove|rm)',
    'grant':    '(?:allow|grant|add)',
    'revoke':   '(?:deny|revoke|remove|rm|delete|del)',
    'to':       '(?:to|on)',
    'from':     '(?:from|on)',
})


@commands.register("^new server (hostname)$")
def new_server(hostname):
    """create a new server by name"""
    return database.new_server(hostname)


@commands.register("^delete server (hostname)$")
def delete_server(hostname):
    """delete an existing server by name"""
    return database.delete_server(hostname)


@commands.register("^new user (username)$")
def new_user(username):
    """create a new user by name"""
    return database.new_user(username)


@commands.register("^delete user (username)$")
def delete_user(username):
    """delete an existing user by name"""
    return database.delete_user(username)


@commands.register("^grant (username) access to (hostname)$")
def grant_access(username, hostname):
    """grant access to a user on an existing server"""
    return database.grant_access(username, hostname)


@commands.register("^revoke (username) access from (hostname)$")
def revoke_access(username, hostname):
    """revoke access to a user from an existing server"""
    return database.revoke_access(username, hostname)


@commands.register("^has (username) access to (hostname)$")
@commands.register("^(username) has access to (hostname)$")
def access_granted(username, hostname):
    """return whether a user has access to an existing server"""
    status = 0 if database.access_granted(username, hostname) else 1
    exit(status)


def parse(command):
    return commands.parse(command)


def help():
    return commands.help()
