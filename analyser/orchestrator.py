import subprocess as sp
from path import Path
from string import Formatter
from meta import *


# collect files :
# output files -> get the entire files
# log files -> same but seek(0, 2) before call function


@boost_fn
def get_stdout(obj):           return obj.stdout
@boost_fn
def get_stderr(obj):           return obj.stderr
@boost_fn
def get_args(obj):             return obj.args
@boost_fn
def get_returncode(obj):       return obj.returncode
@boost_fn
def get_check_returncode(obj): return obj.check_returncode()

def cmd(cmd):
    @boost_fn
    def run_cmd(*input):
        input = ' '.join(input) if len(input) else None
        return sp.run(cmd.split(), input=input, encoding='utf-8', capture_output=True)
    return run_cmd

_formatter = Formatter()

class DefaultFormatList(list):
    def __getitem__(self, pos):
        return list.__getitem__(self, pos) if pos < len(self) else '{}'

class DefaultFormatDict(dict):
    def __getitem__(self, key):
        return dict.__getitem__(self, key) if key in self else '{'+str(key)+'}'


@boost_fn
def pformat(field, *args, **kwargs):
    return _formatter.vformat(field, DefaultFormatList(args), DefaultFormatDict(kwargs))

@boost_fn
class Cmd(Function):
    def __init__(self, args):
        # Will return CompleteProcess object gather all the attributes bellow.
        self._args = args
        self.cp = cmd(args)

        self.stdout =           get_stdout * self.cp
        self.stderr =           get_stderr * self.cp
        self.args =             get_args * self.cp
        self.returncode =       get_returncode * self.cp
        self.check_returncode = get_check_returncode * self.cp

        self.append = Cmd * bf(operator.add) << (self._args + ' ')
        self.format = Cmd * pformat << self._args

        Function.__init__(self, self.cp)

    def __repr__(self):
        return self._args

    def __call__(self, *input):
        return self.cp(*input)

    def __add__(self, arg):
        '''
        operator + allow to append additional arguments at the end of the command
        '''
        return Cmd(self._args + ' ' + arg)

    def __mod__(self, arg):
        '''
        operator % allow to partially format the command with a the provided argument
        '''
        return Cmd(pformat(self._args, arg))

    # def format(self, *args, **kwargs):
    #     '''
    #     Allow to partially format the command with a the provided arguments
    #     '''
    #     return Cmd(pformat(self._args, *args, **kwargs))


def tail_file(file):
    file.seek(0, 2)

def load_and_map(files):
    return dict(map(lambda f:(f.name, f.readlines()), map(open, files)))


class Task(Function):
    def __init__(self, cmd, log_files=None, out_files=None):
        Function.__init__(self, lambda : self.run())
        self.cmd = cmd
        self.log_files = not_none_fwd_or(log_files, [])
        self.out_files = not_none_fwd_or(out_files, [])

        self.res = None

    def run(self):
        # set log file cursors at the end
        dump_map(tail_file, self.log_files)

        result = self.cmd()

        log_data = load_and_map(self.log_files)
        out_data = load_and_map(self.out_files)

        return result, out_data, log_data

    def __call__(self):
        if self.res is None:
            self.res = self.run()
        return self.res

    def force(self):
        self.res = self.run()
        return self.res

    def __repr__(self):
        return repr(self.cmd)



def googleBench(executable, output = None):
    output = not_none_fwd_or(output, filename(executable) + '.json')
    cmd = Cmd(executable + " --benchmark_out=" + output)
    return Task(cmd, out_files=[output])

ls = Cmd('ls')
du = Cmd('du {}')
grep = Cmd('grep {}')

class TaskManager:
    def __init__(self):
        self.tasks = []

    def register(self, task):
        self.tasks.append(task)

    def resolve(self):
        dump_map(apply, self.tasks)

tm = TaskManager()

@boost_fn
def register_task(task):
    tm.register(task)
    return task

r_register_cmd = register_task * Task
r_googleBench = register_task * googleBench

binary_size = lambda exe : du.format(exe).stdout | (bf(str.split) >> '\t') | get >> 0

exe = '../../sandbox/build/benchmark/bench1/SandboxBench1'

gb1 = r_googleBench(exe, 'out.json')

bin_size = r_register_cmd(binary_size(exe))


