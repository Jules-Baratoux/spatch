import json
from json import JSONEncoder
import shelve

import pickle

import database
from splatch.cmdparse import CommandParser

commands = CommandParser(alias={
    'hostname': '(?:\w+)',
    'alias':    '(?:\w+)',
    'filename': '(?:[\w\\/:.-_0-9]+)',
    'username': '(?:\w+)',
    'port-number':     '(?:[0-9]+)',
    'new':      '(?:add|new)',
    'delete':   '(?:delete|del|remove|rm)',
    'grant':    '(?:allow|grant|add)',
    'revoke':   '(?:deny|revoke|remove|rm|delete|del)',
    'to':       '(?:to|on)',
    'from':     '(?:from|on)',
})

@commands.register("^new server (hostname) (port-number)$")
def new_server(hostname, port):
    """create a new server by name and port"""
    return database.new_server(hostname, port)


@commands.register("^delete server (hostname)$")
def delete_server(hostname):
    """delete an existing server by name"""
    return database.delete_server(hostname)


@commands.register("^new user (username) (filename)$")
def new_user(username, filename):
    """create a new user by name and public key filename"""
    return database.new_user(username, filename)


@commands.register("^delete user (username)$")
def delete_user(username):
    """delete an existing user by name"""
    return database.delete_user(username)


@commands.register("^grant (username) access to (hostname) as (alias)$")
def grant_access(username, hostname, alias):
    """grant access to a user on an existing server as a remote user (alias)"""
    return database.grant_access(username, hostname, alias)


@commands.register("^revoke (username) access from (hostname)$")
def revoke_access(username, hostname):
    """revoke access to a user from an existing server"""
    return database.revoke_access(username, hostname)


@commands.register("^(username) has access to (hostname)$")
def access_granted(username, hostname):
    """return whether a user has access to an existing server"""
    status = 0 if database.access_granted(username, hostname) else 1
    exit(status)


class DatabaseJsonEncoder(JSONEncoder):
    def default(self, o):
        if hasattr(o, 'items'):
            return dict(o)
        else:
            return o.__dict__


@commands.register("^dump database to json$")
def json_dump():
    """dump the database in a json format"""
    shelf = shelve.open(database.filename, flag='c')
    print json.dumps(shelf, cls=DatabaseJsonEncoder)
    shelf.close()


@commands.register("^export (users|servers) to (filename)$")
def json_dump(section, filename):
    """export a database section by name to a file given by filename"""
    with open(filename, mode='w+') as fp:
        shelf = shelve.open(database.filename, flag='r')
        pickle.dump(shelf[section], fp)
        shelf.close()


@commands.register("^import (users|servers) from (filename)$")
def json_dump(section, filename):
    """import a database section by name from a file given by filename"""
    with open(filename, mode='r') as fp:
        shelf = shelve.open(database.filename, flag='w')
        new = pickle.load(fp)
        old = database._get_table(section)
        old.update(new)
        shelf[section] = old
        shelf.close()


def parse(command):
    return commands.parse(command)


def help():
    return commands.help()
