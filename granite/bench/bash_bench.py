from utils.functional import boost_fn, bf, list_at
from utils.command import du

from .bench_utils import Bench

binary_size_1 = lambda exe : du.format(exe).stdout | (bf(str.split) >> '\t') | list_at >> 0

@boost_fn
def binary_size_format_1(size):
    return {
        'type' : 'binary_size',
        'version' : 1,
        'value' : size}


bench = {
    1 : Bench(binary_size_1, binary_size_format_1)}

current = 1

def get_bench(version = current):
    return bench[version]