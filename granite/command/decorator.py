from pampy import match, _

from cliff.command import Command
from cliff.commandmanager import CommandManager
from collections.abc import Iterable
from granite.utils.functional import boost_fn, dump_map

# Static instance that reference all application commands
# It could be replace by setuptools entry points but this solution 
# needs to put some logic in setup.py that is W(R)ONG on so many levels !
command_manager = CommandManager('greet')

def advertise_command(name, command):
    '''Add the given command to the manager with the given name'''
    command_manager.add_command(name, command)

def simple_action(fn):
    '''Cast a pure function to a method but discard the instance (self) argument'''
    def simple_action_impl(self, args):
        return fn(**vars(args))
    return simple_action_impl

def app_action(fn):
    '''Cast a pure function to a method but provide app, app_args, cmd_name
    from instance (self)'''
    def app_action_impl(self, args):
        return fn(self.app, self.app_args, self.cmd_name, **vars(args))
    return app_action_impl

@boost_fn
def parse_args(parse, args):
    match(args,
        # argument define by a name 
        str,         lambda name : parse.add_argument(name),
        # argument with a name and options
        (str, dict), lambda name, options : parse.add_argument(name, **options),
        # Range of arguments : recursive parsing
        Iterable,    lambda range : dump_map(parse_args << parse, range),
        # Unknown structure : ignore with an error message
        _,           lambda value : print(f'Error, cannot parse : {value}')
    )

def get_parser(args):
    def get_parser_impl(self, prog_name):
        parser = super(type(self), self).get_parser(prog_name)
        if args is not None:
            parse_args(parser, args)
        return parser
    return get_parser_impl

def make_cmd(name, action, args = None, doc = None):
    '''Generate a type with the given name that will invoke the callable fn'''
    return type(f'{name}_cmd', (Command,), {
        'take_action' : action,
        'get_parser'  : get_parser(args),
        '__doc__'     : doc})

def simple_command(name, args = None, doc = None):
    '''Decorator that advertise and forward the function'''
    def simple_command_impl(fn):
        advertise_command(name, make_cmd(name, simple_action(fn), args, doc))
        return fn
    return simple_command_impl

def app_command(name, args = None, doc = None):
    '''Decorator that advertise and forward the function'''
    def app_command_impl(fn):
        advertise_command(name, make_cmd(name, app_action(fn), args, doc))
        return fn
    return app_command_impl

def granite_command(name):
    '''Decorator that advertise and forward the Command class'''
    def granite_command_impl(cls):
        advertise_command(name, cls)
        return cls
    return granite_command_impl