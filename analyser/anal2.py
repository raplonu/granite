import json
import statistics
from functools import partial
import numpy as np
from sklearn.linear_model import LinearRegression
import operator

dump_map = lambda func, *args : (lambda *args : None)(*map(func, *args))

def constant_function(value):
    return lambda : value


def partial_callable(fn, *cargs):
    return partial(fn, *map(lambda c: c(), cargs))

def map_callable(fn, *cargs):
    return map()

class lazy_get:
    def __init__(self, data, key):
        self.call = constant_function(data[key]) if has_key(data, key) else None
            
    def or_compute(slef, f, *args):
        if self.call is None:
            self.call = partial_callable(f, *args)

        return self