from cliff.command import Command
from cliff.commandmanager import CommandManager

command_manager = CommandManager('greet')

def advertise_command(name, command):
    '''Add the given command to the manager this the given name'''
    command_manager.add_command(name, command)

def make_cmd(name, fn, doc = None):
    '''Generate a type with the given name that will invoke the callable fn'''
    return type('{}_cmd'.format(name), (Command,), {
        'take_action': lambda self, _: fn(),
        '__doc__':doc})

def granite_command(name):
    '''Decorator that advertise and forward the Command class'''
    def granite_command_impl(cls):
        advertise_command(name, cls)
        return cls
    return granite_command_impl


def simple_command(name, doc = None):
    '''Decorator that advertise and forward the function'''
    def simple_command_impl(fn):
        advertise_command(name, make_cmd(name, fn, doc))
        return fn
    return simple_command_impl

def system_command(name, doc = None):
    '''Decorator that advertise a function that take the system as argument'''
    def system_command_impl(fn):
        lambda system : advertise_command(name, make_cmd(name, bf(fn) << system, doc))


        return fn
    return system_command_impl


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