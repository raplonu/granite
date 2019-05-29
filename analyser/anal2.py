import functools as ft
import funcy as fc

import  boltons.cacheutils as cu

import json
import csv

import numpy as np
import statistics
from sklearn.linear_model import LinearRegression

import operator

dump_map = lambda func, *args : (lambda *args : None)(*map(func, *args))

@fc.decorator
def partialize(fn):
    return fc.partial(fn)

decor_and_wraps = lambda fn, *decos: fc.compose(ft.wraps(fn), *decos)

@ft.wraps(cu.cached)
def cached(cache, scoped=True, typed=False, key=None):
    return lambda fn : decor_and_wraps(fn,
        cu.cached(cache, scoped, typed, key))(fn) 

def partialize_cached(cache, scoped=True, typed=False, key=None):
    return fc.compose(partialize, cached(cache, scoped, typed, key))

file_data_cache = cu.LRU(max_size=128)

@decor_and_wraps(json.load, partialize_cached(file_data_cache))
def json_load(filename):
    print("Loading JSON file :{}".format(filename))
    return json.load(open(filename))

@partialize_cached(file_data_cache)
def csv_load(filename):
    print("Loading CSV file :{}".format(filename))
    return csv.reader(open(filename))

def cached_compose(cache, *funs):
        @partialize_cached(cache)
        def compose_apply(funs, *args):
                return fc.compose(*funs)(*args)
        return compose_apply(funs)

def cached_rcompose(cache, *funs):
        @partialize_cached(cache)
        def rcompose_apply(funs, *args):
                return fc.rcompose(*funs)(*args)
        return rcompose_apply(funs)

@partialize
def print_forward(comment, x):
        print(comment)
        return x

@partialize
def get(key, seq):
    return seq[key]

@partialize
def equal_to(arg1, arg2):
    return arg1 == arg2

first_filter = partialize(fc.compose(fc.first, fc.filter))

@partialize
def select_values(key, seq):
    return [s[key] for s in seq]

@partialize
def find_pos(value, seq):
    return list(seq).index(value)

def field_match(key, value):
    return fc.compose(equal_to(value), get(key))

def match_at(value, pos):
    return fc.compose(equal_to(value), get(pos))



jdata = json_load("data/fun1_reg.json")
cdata = csv_load("data/fun1_runtime.csv")

find_bench_by_name = lambda name : fc.rcompose(get("benchmarks"), first_filter(field_match("name", name)))

prop_cache = cu.LRU(max_size=2048)

fun1_jbench = cached_rcompose(prop_cache, jdata,
        find_bench_by_name("BM_Fun1"), print_forward('get bench'))

fun1_mean = cached_rcompose(prop_cache, fun1_jbench,
        get("real_time"), print_forward('get real_time'))

fun1_rep = cached_rcompose(prop_cache, fun1_jbench,
        get("repetitions"), print_forward('get repetitions'))

fun1_cbench = cached_rcompose(prop_cache, cdata,
        first_filter(match_at("BM_Fun1", 0)))

fun1_run = cached_rcompose(prop_cache, fun1_cbench,
        get(2))

fun1_cpu = cached_rcompose(prop_cache, fun1_cbench,
        get(3))




# def partialize(*p_args, **p_kwargs):
#     def inter_partialize(fn):
#         def wrapper_partialize(*args, **kwargs):
#             return fn(*p_args, *args, **kwargs, **p_kwargs)
#         return wrapper_partialize
#     return inter_partialize




# def ft.partial_callable(fn, *cargs):
#     return ft.partial(fn, *map(lambda c: c(), cargs))

# def map_callable(fn, *cargs):
#     return map()

# class lazy_get:
#     def __init__(self, data, key):
        # self.call = constant_function(data[key]) if has_key(data, key) else None
            
#     def or_compute(slef, f, *args):
#         if self.call is None:
#             self.call = ft.partial_callable(f, *args)

#         return self


