import re

command_descriptions = []


class Namespace(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def register(pattern, alias={}):
    """
    Generate a @decorator to register a command argument pattern.

    :rtype: @decorator
    """
    def decorator(function):

        local = Namespace(pattern=pattern)

        for key, value in alias.items():
            local.pattern = local.pattern.replace(key, value)
        regex = re.compile(local.pattern)
        info = (pattern, regex, function, function.__doc__)
        command_descriptions.append(info)  # 47
        return function

    return decorator


def process(command):
    for pattern, regex, function, doc in command_descriptions:  # 47
        match = regex.match(command)
        if match:
            return function(match)

    raise ValueError('no matching command found')


def help():
    width = 0
    commands = []

    for pattern, regex, function, doc in command_descriptions:  # 47
        string = pattern.lstrip('^').rstrip('$')
        command = re.sub('\((\w+)\)', '<\\1>', string)
        commands.append((command, doc))
        width = max(len(command), width)

    return "\n".join(["%-*s  -- %s" % (width, command, doc) for command, doc in commands])
