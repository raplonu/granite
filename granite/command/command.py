from cliff.command import Command
from cliff.commandmanager import CommandManager

command_manager = CommandManager('greet')

def add_command(name, command):
    command_manager.add_command(name, command)

def granite_command(name):
    def granite_command_impl(cls):
        add_command(name, cls)
        return cls
    return granite_command_impl


def simple_command(name, doc = None):
    def simple_command_impl(fn):
        @granite_command(name)
        class Simple(Command):
            def take_action(self, parsed_args):
                fn()

        Simple.__doc__ = doc
        return Simple
    return simple_command_impl



@granite_command('hello')
class Hello(Command):
    """Say hello"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name')
        return parser

    def take_action(self, args):
        print('Hello {}'.format(args.name))


@granite_command('bye')
class Bye(Command):
    """Say bye"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name')
        return parser

    def take_action(self, args):
        print('Bye {}'.format(args.name))


granite_name = R'''
                            _..._  .--.             __.....__
  .--./)                  .'     '.|__|         .-''         '.
 /.''\\  .-,.--.         .   .-.   .--.    .|  /     .-''"'-.  `.
| |  | | |  .-. |   __   |  '   '  |  |  .' |_/     /________\   \
 \`-' /  | |  | |.:--.'. |  |   |  |  |.'     |                  |
 /("'`   | |  | / |   \ ||  |   |  |  '--.  .-\    .-------------'
 \ '---. | |  '-`" __ | ||  |   |  |  |  |  |  \    '-.____...---.
  /'""'.\| |     .'.''| ||  |   |  |__|  |  |   `.             .'
 ||     || |    / /   | ||  |   |  |     |  '.'   `''-...... -'
 \'. __//|_|    \ \._,\ '|  |   |  |     |   /
  `'---'         `--'  `"'--'   '--'     `'-'
'''

@simple_command('echo', 'show granite l33t name')
def echo():
    print(granite_name)
### Credit to http://patorjk.com/software/taag/