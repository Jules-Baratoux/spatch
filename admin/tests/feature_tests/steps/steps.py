# coding=utf-8
from behave import *

@step('we stop the process')
def step_impl(context):
    context.process.status = context.process.stop()
