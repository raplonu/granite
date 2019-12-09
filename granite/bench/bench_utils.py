from granite.utils.functional import boost_fn, Function, dump_map, fwd, apply

from pampy import match, _
from collections.abc import Iterable, Iterator, Mapping
from types import GeneratorType

class Bench:
    def __init__(self, bench, format):
        self.bench = bench
        self.format = format

    def format(self, *args, **kwargs):
        return (self.format <= self.bench)(*args, **kwargs)

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

def process_container(d):
    '''Will explore containers to a json compatible data.
    '''
    return match(d,
        # Special handle for str that is instance of Iterable but
        # does not need to be processed.
        str, fwd,
        # Handle for Mapping types, we do not want to check if
        # keys are callable. We only iterate on values.
        Mapping, lambda m : type(m)(zip(m.keys(), process_container(m.values()))),
        Iterable, lambda i : list(map(process_container, i)),
        callable, apply,
        _, fwd)


@boost_fn
def format_bench(data, bench_type, bench_version):
    return dict(data=data, bench_type=bench_type, bench_version=bench_version)