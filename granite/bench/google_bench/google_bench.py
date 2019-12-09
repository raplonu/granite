from granite.utils.functional import boost_fn, not_none_fwd_or
from granite.utils.command import Cmd
from granite.utils.path import filename

from .bench_utils import Bench
from . import google_bench_1

# The bench function
def google_bench_cmd(exe_path, output_file, bench_list = []):
    cmd = Cmd('{} --benchmark_out={} --benchmark_filter="{}"'.format(
        exe_path, output_file, '|'.join(bench_list)))

    cmd()
    return output_file

# The bench formater 
@boost_fn
def format(bench_file, bench_name):
    return {'file' : bench_file,
        'bench_name' : bench_name}

# The list that describes 
bench = {
    1 : google_bench_1.properties,
}

current_version = 1
name = 'google_bench'

class GoogleBench:
    def __init__(self, exe_path, output_file):
        self.fns = []
        self.bench_proc = call_once(google_bench_cmd, exe_path, output_file, self.fns)

    def register(self, bench_name):
        self.fns.append(bench_name)

        return format_bench.rpartial(name, current_version) * (format >> bench_name) * self

    def __call__(self):
        return self.bench_proc()


def make_bench(exe_path, output_file):
    return GoogleBench(exe_path, output_file)
