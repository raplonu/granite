import os

from utils.functional import boost_fn, bf, list_at
# from utils.command import du


from .bench_utils import Bench
from . import bash_bench_1

# binary_size = lambda exe : du.format(exe).stdout | (bf(str.split) >> '\t') | list_at >> 0

def binary_size(exe_path):
    return os.stat(exe_path).st_size



bench = {
    1 : bash_bench_1.properties,
}


current_version = 1
name = 'bash_bench'

def make_bench(exe_path):
    return 