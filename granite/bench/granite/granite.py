from time import time
import numpy as np
from granite.utils.functional import b_map, boost_fn, bf
from ..bench_utils import make_bench

# Range with exponential growing
exp_range = (b_map << (lambda x : 2**x)) * range

def measure(fn):
    t = time()
    fn()
    return time() - t

def measure_mean(iter, fn):
    return np.average([measure(fn) for _ in range(iter)])

# maximum bench time in sec
MAX_TIME = 1
# maximum bench iteration 2**20 -> 1048576
MAX_POWER = 20

@boost_fn
def bench(fn):
    t_start = time()
    times = []
    iters = []

    # Fist call for cache issue
    fn()

    for n_iter in exp_range(MAX_POWER):
        times.append(measure_mean(n_iter, fn))
        iters.append(n_iter)
        if time() - t_start > MAX_TIME:
            break

    # np.XXX algorithms cannot work with generators.
    # times and iters must have a know size like list.
    return np.average(times, weights=iters), np.sum(iters)

@boost_fn
def format(output):
    '''Return a result formated for granite'''
    print(f'format {output}')
    return {'mean' : output[0]}

f_bench = make_bench(bench, format)