import json
import statistics
import functools as ft
import numpy as np
from sklearn.linear_model import LinearRegression
import operator
import  boltons.cacheutils as cu
import funcy

dump_map = lambda func, *args : (lambda *args : None)(*map(func, *args))

def constant_function(value):
    return lambda : value

def compose_deco(*decos):
    def composed(fn):
        for deco in reversed(decos):
            fn = deco(fn)
        return fn
        # return funcy.compose(fn, *reversed(decos))
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
def json_load(filename):
    print("Loading JSON file :{}".format(filename))
    return json.load(open(filename))


prop_cache = cu.LRU(max_size=2048)

@lazy_cached(prop_cache)
def prop_access(jdata_loader, property_acc):
    res = property_acc(jdata_loader())
    print("Getting result : {}".format(res))
    return res


def getter(key):
    return lambda data: data[key]

def is_value(value):
    return lambda data: value == data

def first(predicate):
    return lambda data: next((d for d in data if predicate(d)), None)

def flatter(key):
    return lambda data: [d[key] for d in data]

def access_to(*getters):
    def wrapper_access_to(data):
        for getter in getters:
            data = getter(data)
        return data
    return wrapper_access_to

jdata = json_load("data/fun1_reg.json")

def match_field(key, value):
    return funcy.compose(is_value(value), getter(key))

fun1_mean = prop_access(jdata,
    access_to(
        getter("benchmarks"),
        first(match_field("name", "BM_Fun1")),
        getter("real_time")))



fun1_rep = prop_access(jdata,
    access_to(
        getter("benchmarks"),
        first(match_field("name", "BM_Fun1")),
        getter("repetitions")))





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


