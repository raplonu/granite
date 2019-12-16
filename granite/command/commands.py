from .decorator import simple_command, app_command, granite_command, Command

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
### Credit to http://patorjk.com/software/taag/

@simple_command('echo', None, 'show granite l33t name')
def echo():
    print(granite_name)


@app_command('instance', None, 'show granite instance l33t name')
def echo(app, *_):
    print(f"App instance : {app}")


@granite_command('hello')
class Hello(Command):
    """Say hello"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name')
        return parser

    def take_action(self, args):
        print(f'Hello {args.name}')


@granite_command('bye')
class Bye(Command):
    """Say bye"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name')
        return parser

    def take_action(self, args):
        print(f'Bye {args.name}')


@app_command('data', None, 'display raw data structure')
def show_data(app, *_):
    print(app.system.data)

def print_iter(iter, prefix = '- ', delim = ''):
    for e in iter:
        print(f'{prefix}{e}{delim}')


@app_command('names', None, 'display name list')
def show_name(app, *_):
    print_iter(app.system.names())


@app_command('benchs', None, 'display benchs list')
def show_benchs(app, *_):
    print_iter(app.system.benchs())

@app_command('exec', None, 'execute benchs list')
def show_benchs(app, *_):
    app.system.exec()