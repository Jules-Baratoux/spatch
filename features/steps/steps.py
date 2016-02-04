# coding=utf-8
import os

from behave import *

import database
import splatch


def python(command):
    return os.system('python %s' % command)


def script(command):
    return python("%s %s" % (os.path.dirname(splatch.__file__), command))


@given('a username public key pair')
def step_impl(context):
    context.username = 'user%i' % id(context)
    context.public_key_filename = 'pub%i' % id(context)


@given('an alias')
def step_impl(context):
    context.alias = 'alias%i' % id(context)


@given('a hostname port pair')
def step_impl(context):
    context.hostname = 'server%i' % id(context)
    context.port = '%s' % str(id(context))[:4]


@given('the server exists')
def step_impl(context):
    script('new server %s %s' % (context.hostname, context.port))


@given('the database is reset')
def step_impl(context):
    import database
    os.system('rm --force "%s"' % database.filename)


@given('the user exists')
def step_impl(context):
    script('new user %s %s' % (context.username, context.public_key_filename))


@when('I grant the user access to the server')
def grant_access(context):
    script('grant %s access to %s as %s' % (context.username, context.hostname, context.alias))


@then('the user has access to the server')
def step_impl(context):
    assert script('%s has access to %s' % (context.username, context.hostname)) == 0


@given('the user has access to the server')
def step_impl(context):
    grant_access(context)


@then('the user does not have access to the server')
def step_impl(context):
    assert script('%s has access to %s' % (context.username, context.hostname)) == 1


@when('I revoke the user access from the server')
def step_impl(context):
    script('revoke %s access from %s' % (context.username, context.hostname))


@when('I access the user by name')
def step_impl(context):
    context.result = database.user(context.username)


@then('a valid User instance is returned')
def step_impl(context):
    assert context.result.username == context.username
    assert context.result.public_key_filename == context.public_key_filename


@when("I request the user's granted_servers list")
def step_impl(context):
    context.result = database.granted_servers(context.username)


@then("a valid list is returned")
def step_impl(context):
    hostname, port, alias = context.result[0]
    assert hostname == context.hostname
    assert port == context.port
    assert alias == context.alias


@then("an empty list is returned")
def step_impl(context):
    assert len(context.result) == 0
