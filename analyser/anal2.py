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
cdata = csv_load("data/fun2_reg.csv")

json_find_bench_by_name = lambda name : fc.rcompose(get("benchmarks"), first_filter(field_match("name", name)))

csv_find_bench_by_name = lambda name : first_filter(match_at(name, 0))

regular_google = {
        'mean' : get('real_time'),
        'bench' : json_find_bench_by_name
}

regular_granite = {
        'mean' : fc.rcompose(get(2), float, int),
        'bench': csv_find_bench_by_name

}

regular_bench = {
        'google'  : regular_google,
        'granite' : regular_granite
}

runtime_granite = {
        'raw' : fc.identity,
        'bench' : fc.identity
}

runtime_bench = {
        'granite' : runtime_granite
}

benchmarks = {
        'regular' : regular_bench,
        'runtime' : runtime_bench
}


prop_cache = cu.LRU(max_size=2048)

fun1_jbench = cached_rcompose(prop_cache, jdata,
        json_find_bench_by_name("BM_Fun1"))

fun1_mean = cached_rcompose(prop_cache, fun1_jbench,
        regular_google['mean'])

# fun1_rep = cached_rcompose(prop_cache, fun1_jbench,
#         get("repetitions"), print_forward('get repetitions'))



fun2_cbench = cached_rcompose(prop_cache, cdata,
        csv_find_bench_by_name("BM_Fun2"))

fun2_mean = cached_rcompose(prop_cache, fun2_cbench,
        regular_granite['mean'])

# fun2_cpu = cached_rcompose(prop_cache, fun2_cbench,
#         get(3), float, int)