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

@boost_fn
def call_and_log(fn, out_files, log_files):
        dump_map(tail_file, log_files)

        result = fn()

        log_data = load_and_map(log_files)
        out_data = load_and_map(out_files)

        return result, out_data, log_data



class Task(Function):
    def __init__(self, cmd, log_files=None, out_files=None):
        self.cmd = cmd
        self.log_files = not_none_fwd_or(log_files, [])
        self.out_files = not_none_fwd_or(out_files, [])

        Function.__init__(self, call_once(call_and_log,
            self.cmd, self.out_files, self.log_files))

    def __repr__(self):
        return repr(self.cmd)


@boost_fn
def google_bench_cmd(exe_path, bench_file = None):
    bench_file = not_none_fwd_or(bench_file, filename(exe_path) + '.json')
    cmd = Cmd(exe_path + " --benchmark_out=" + bench_file)
    cmd()
    return bench_file

@boost_fn
def format_google_bench(bench_file, bench_name):
    return {'type' : 'regular',
        'generator' : 'google',
        'file' : bench_file,
        'bench_name' : bench_name}

binary_size = lambda exe : du.format(exe).stdout | (bf(str.split) >> '\t') | get >> 0

@boost_fn
def format_binary_size(size):
    return {'type' : 'binary_size',
        'value' : size}

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

register_once = register_task * call_once
# r_register_cmd = register_task * Task
# r_googleBench = register_task * google_bench_cmd


exe = '../../sandbox/build/benchmark/bench1/SandboxBench1'

gb1 = format_google_bench <= register_once(google_bench_cmd, exe, 'out.json')

bin_size = format_binary_size <= register_once(binary_size(exe))

def process_dict(d):
    return match(d,
        dict, lambda d : dict(zip(d.keys(), process_dict(list(d.values())))),
        list, lambda l : list(map(process_dict, l)),
        callable, apply
    )

res = {}

fun1 = []
fun1.append(gb1 << 'BM_Fun1')
res['fun1'] = fun1

binary = []
binary.append(bin_size)
res['binary'] = binary

