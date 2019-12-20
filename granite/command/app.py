
from cliff.app import App
from cliff.command import Command

from .decorator import command_manager

from granite.system.system import System
from granite.utils.functional import boost_fn, bf, b_print, map_apply

#import commands to register all commands into the manager
from . import commands

class GraniteApp(App):

    def __init__(self, context = None, bdd_conn = None):
        # Create the system.
        self.system = System(context, bdd_conn)

        super(GraniteApp, self).__init__(
            description='Granite command app',
            version='0.1',
            command_manager=command_manager,
            deferred_help=True)



    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug(f'prepare_to_run_command {cmd.__class__.__name__}')

    def clean_up(self, cmd, result, err):
        self.LOG.debug(f'clean_up {cmd.__class__.__name__}')
        if err:
            self.LOG.debug(f'got an error: {err}')

    def register(self, data):
        self.system.register(data)

    def register_benchs(self, name, benchs):
        self.system.register_benchs(name, benchs)

    def register_bench(self, name, bench_name, bench):
        self.system.register_bench(name, bench_name, bench)


# def register_system_method(system):
#     simple_command('data', 'display raw data structure')(show_data << system)
#     # simple_command('result', 'display raw result structure')(show_result << system)
#     simple_command('run', 'process data structure')(
#         bf(System.run) << system)