import os
import sys

from admin import commands

def main():
    commands_line = ' '.join(sys.argv[1:])
    name = os.path.basename(sys.path[0])

    try:
        commands.parse(commands_line)
    except ValueError:
        print "usage: %s <command>\n\ncommands:\n%s" % (
        name, "\n".join("\t%s" % line for line in commands.help().split('\n')))


if __name__ == '__main__':
    main()
