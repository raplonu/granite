
from cliff.app import App
from cliff.command import Command

from .command import command_manager, simple_command
from granite.system.system import System
from granite.utils.functional import boost_fn

@boost_fn
def show_data(obj):
    print(obj.data)

@boost_fn
def show_result(obj):
    print(obj.result)


@boost_fn
def run_data(obj):
    obj.run()

def register_system_method(system):
    simple_command('data', 'display raw data structure')(show_data << system)
    simple_command('result', 'display raw result structure')(show_result << system)
    simple_command('run', 'process data structure')(run_data << system)

class GraniteApp(App):

    def __init__(self):
        super(GraniteApp, self).__init__(
            description='Granite command app',
            version='0.1',
            command_manager=command_manager,
            deferred_help=True,
            )
        self._system = System()

        register_system_method(self._system)

        # @simple_command('data', 'display raw data structure')
        # def fun():
        #     print(self._system.data)

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



