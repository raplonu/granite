from granite.utils.functional import boost_fn, not_none_fwd_or
from granite.utils.command import Cmd
from granite.utils.path import filename

from .bench_utils import Bench

@boost_fn
def google_bench_cmd_1(exe_path, bench_file = None):
    bench_file = not_none_fwd_or(bench_file, filename(exe_path) + '.json')
    cmd = Cmd(exe_path + " --benchmark_out=" + bench_file)
    cmd()
    return bench_file

@boost_fn
def google_bench_format_1(bench_file, bench_name):
    return {'type' : 'regular',
        'generator' : 'google',
        'version' : 1,
        'file' : bench_file,
        'bench_name' : bench_name}

bench = {
    1 : Bench(google_bench_cmd_1, google_bench_format_1)}

current = 1

def get_bench(version = current):
    return bench[version]