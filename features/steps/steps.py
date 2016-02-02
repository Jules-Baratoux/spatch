# coding=utf-8
import os

from behave import *
import admin


def python(command):
    return os.system('python ' + command)


@given('the admin script')
def step_impl(context):
    context.script_filename = admin.__file__


@given('a username')
def step_impl(context):
    context.username = 'jules'


@given('a hostname')
def step_impl(context):
    context.hostname = 'server42'


@given('the server exists')
def step_impl(context):
    python('admin new server %s' % context.hostname)


@given('the database is reset')
def step_impl(context):
    import database
    os.system('rm "%s"' % database.filename)


@given('the user exists')
def step_impl(context):
    python('admin new user %s' % context.username)


@when('I grant the user access to the server')
def step_impl(context):
    python('admin grant %s access to %s' % (context.username, context.hostname))


@then('the user has access to the server')
def step_impl(context):
    assert python('admin has %s access to %s' % (context.username, context.hostname)) == 0


@then('the user does not have access to the server')
def step_impl(context):
    assert python('admin has %s access to %s' % (context.username, context.hostname)) == 1


@when('I revoke the user access from the server')
def step_impl(context):
    python('admin revoke %s access from %s' % (context.username, context.hostname))
