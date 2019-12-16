from granite.utils.functional import boost_fn, bf, Function, dump_map, fwd, apply, return_function

from pampy import match, _
from collections.abc import Iterable, Iterator, Mapping
from types import GeneratorType


def make_bench(bench, format):
    def make_bench_impl(fn, *args, **kwargs):
        return bf(format) * bf(bench) << (lambda : fn(*args, **kwargs))
    return make_bench_impl

class Bench:
    def __init__(self, bench, format):
        self.bench = bench
        self.format = format

    def format(self, *args, **kwargs):
        return self.format(self.bench(), *args, **kwargs)

def tail_file(file):
    '''Change the stream position to the end of the file.'''
    # Set the offset to 0 from the end of the file (2).
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

        super().__init__(self, call_once(call_and_log,
            self.cmd, self.out_files, self.log_files))

    def __repr__(self):
        return repr(self.cmd)

def process_container(d):
    '''Will explore containers to a json compatible data.'''
    return match(d,
        # Special handle for str that is instance of Iterable but
        # does not need to be processed.
        str,      fwd,
        # Handle for Mapping types, we do not want to check if
        # keys are callable. We only iterate on values.
        Mapping,  lambda m : type(m)(zip(m.keys(), process_container(m.values()))),
        Iterable, lambda i : list(map(process_container, i)),
        callable, apply,
        _,        fwd)


@boost_fn
def format_bench(data, bench_type, bench_version):
    return dict(data=data, bench_type=bench_type, bench_version=bench_version)

@boost_fn
def rename_result(data, old_name, new_name):
    data[new_name] = data.pop(old_name)
    return data

@boost_fn
def rename_results(data, old_names, new_names):
    dump_map(rename_result << data, old_names, new_names)
    return data

@boost_fn
def rename_bench(old_name, new_name):
    rename_fun = match((old_name, new_name),
        (str, str),           return_function(rename_result),
        (Iterable, Iterable), return_function(rename_results),
        (_, _),               lambda a, b : print(f'{a} & {b} must be both str or iterable'))
    
    return rename_fun.rpartial(old_name, new_name)

@boost_fn
def drop_result(data, name):
    data.pop(name)
    return data

@boost_fn
def drop_results(data, names):
    dump_map(drop_result << data, names)
    return data

@boost_fn
def drop_bench(name):
    drop_fun = match(name,
        str, return_function(drop_result),
        Iterable, return_function(drop_results),
        _, lambda a : print(f'{a} must be str or iterable'))
    
    return drop_fun >> name
