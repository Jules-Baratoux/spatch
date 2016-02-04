import os
import sys

from admin import commands


def usage():
    name = os.path.basename(sys.path[0])
    return """usage:
    %s <command>

commands:
%s""" % (name, "\n".join("    %s" % line for line in commands.help().split('\n')))


def main():
    commands_line = ' '.join(sys.argv[1:])

    try:
        task = commands.parse(commands_line)
    except ValueError:
        print usage()
    else:
        task()


if __name__ == '__main__':
    main()
