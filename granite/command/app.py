
from cliff.app import App
from cliff.command import Command

from .command import command_manager, simple_command
from granite.system.system import System
from granite.utils.functional import boost_fn, bf, b_print, map_apply

system_commands = []

class GraniteApp(App):

    def __init__(self):
        # Create the system.
        self._system = System()

        self.command_manager = CommandManager('granite app')

        # Generate the commands with the system instance and advertise them.
        map_apply(system_commands << self._system)

        super(GraniteApp, self).__init__(
            description='Granite command app',
            version='0.1',
            command_manager=command_manager,
            deferred_help=True,
            )

    def initialize_app(self, argv):
        self.LOG.info('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.info('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.info('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.info('got an error: %s', err)

    def register(self, data):
        self._system.register(data)

    def register_benchs(self, name, benchs):
        self._system.register_benchs(name, benchs)

    def register_bench(self, name, bench):
        self._system.register_bench(name, bench)


    def advertise_command(self, name, command):
        self.command_manager.add_command(name, command)

    def advertise_simple_command(self, name, fn, doc = None):
        self.


    def advertise_system_cmd(self, name, cmd, doc = None):
        '''Advertise a cmd that use system data'''
        simple_command(name, doc)(bf(cmd) << self._system)

def register_system_function(system):


@boost_fn
def show_data(obj):
    print(obj.data)



def register_system_method(system):
    simple_command('data', 'display raw data structure')(show_data << system)
    # simple_command('result', 'display raw result structure')(show_result << system)
    simple_command('run', 'process data structure')(
        bf(System.run) << system)