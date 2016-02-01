import re


class CommandParser(object):
    def __init__(self, alias={}):
        self.command_descriptions = []
        self.alias = alias

    def register(self, *args, **kwargs):
        """
        Generate a @decorator to register a command argument pattern.

        :rtype: @decorator
        """

        def prepare(function):
            pattern = kwargs.get('pattern', args[0])
            alias = kwargs.get('alias', self.alias)
            doc = kwargs.get('doc', function.__doc__)

            self.__pattern = pattern  # 21

            for key, value in alias.items():
                self.__pattern = self.__pattern.replace(key, value)  # 21
            regex = re.compile(self.__pattern)
            info = (pattern, regex, function, doc)
            self.command_descriptions.append(info)  # 47
            del self.__pattern  # 21

        try:
            function = kwargs['function']
        except KeyError:

            def decorator(wrapped):
                prepare(wrapped)
                return wrapped

            return decorator

        else:
            prepare(function)

    def parse(self, command):
        for pattern, regex, function, doc in self.command_descriptions:  # 47
            match = regex.match(command)
            if match:
                def task():
                    return function(*match.groups(), **match.groupdict())

                return task

        raise ValueError('no matching command found')

    def help(self):
        width = 0
        commands = []

        for pattern, regex, function, doc in self.command_descriptions:  # 47
            string = pattern.lstrip('^').rstrip('$')
            command = re.sub('\((\w+)\)', '<\\1>', string)
            commands.append((command, doc))
            width = max(len(command), width)

        return "\n".join(["%-*s  -- %s" % (width, command, doc) for command, doc in commands])
