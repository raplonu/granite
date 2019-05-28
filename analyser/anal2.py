import json
import statistics
import functools as ft
import numpy as np
from sklearn.linear_model import LinearRegression
import operator
import  boltons.cacheutils as cu

dump_map = lambda func, *args : (lambda *args : None)(*map(func, *args))

def constant_function(value):
    return lambda : value

def compose_deco(*decos):
    def composed(fn):
        for deco in reversed(decos):
            fn = deco(fn)
        return fn
    return composed

decor_and_wraps = lambda fn, *decos: compose_deco(ft.wraps(fn), *decos)

def lazy(fn):
    @ft.wraps(fn)
    def wrapper_lazy(*args, **kwargs):
        return ft.partial(fn, *args, **kwargs)
    return wrapper_lazy

@ft.wraps(cu.cached)
def cached(cache):
    def inter_cached(fn):
        @decor_and_wraps(fn, cu.cached(cache))
        def wrapper_cached(*args, **kwargs):
            return fn(*args, **kwargs)
        return wrapper_cached
    return inter_cached

lazy_cached = lambda cache : compose_deco(lazy, cached(cache))

json_data_cache = cu.LRU(max_size=128)

@decor_and_wraps(json.load, lazy_cached(json_data_cache))
def jdata_load(filename):
    print("Loading JSON file :{}".format(filename))
    return json.load(open(filename))


prop_cache = cu.LRU(max_size=2048)

@lazy_cached(prop_cache)
def prop_access(jdata_loader, property_acc):
    res = property_acc(jdata_loader())
    print("Getting result : {}".format(res))
    return res




# def ft.partial_callable(fn, *cargs):
#     return ft.partial(fn, *map(lambda c: c(), cargs))

# def map_callable(fn, *cargs):
#     return map()

# class lazy_get:
#     def __init__(self, data, key):
#         self.call = constant_function(data[key]) if has_key(data, key) else None
            
#     def or_compute(slef, f, *args):
#         if self.call is None:
#             self.call = ft.partial_callable(f, *args)

#         return self


