import functools as ft
import funcy as fc
from funcy import compose, rcompose
from path import Path

import  boltons.cacheutils as cu

import json
import csv

import numpy  as np
import pandas as pd
import xarray as xr

import matplotlib.pyplot as plt

import statistics
from sklearn.linear_model import LinearRegression

import operator

plt.ion()

print('Hello, welcome to ...')
print('''
   ____    ,---.   .--.   ____      .---.       ____     __  .-'\''-.     .-''-.  .-------.     
 .'  __ `. |    \  |  | .'  __ `.   | ,_|       \   \   /  // _     \  .'_ _   \ |  _ _   \    
/   '  \  \|  ,  \ |  |/   '  \  \,-./  )        \  _. /  '(`' )/`--' / ( ` )   '| ( ' )  |    
|___|  /  ||  |\_ \|  ||___|  /  |\  '_ '`)       _( )_ .'(_ o _).   . (_ o _)  ||(_ o _) /    
   _.-`   ||  _( )_\  |   _.-`   | > (_)  )   ___(_ o _)'  (_,_). '. |  (_,_)___|| (_,_).' __  
.'   _    || (_ o _)  |.'   _    |(  .  .-'  |   |(_,_)'  .---.  \  :'  \   .---.|  |\ \  |  | 
|  _( )_  ||  (_,_)\  ||  _( )_  | `-'`-'|___|   `-'  /   \    `-'  | \  `-'    /|  | \ `'   / 
\ (_ o _) /|  |    |  |\ (_ o _) /  |        \\       /     \       /   \       / |  |  \    /  
 '.(_,_).' '--'    '--' '.(_,_).'   `--------` `-..-'       `-...-'     `'-..-'  ''-'   `'-'   
                                                                                               
''')


@fc.decorator
def partialize(fn):
    return fc.partial(fn)

# Parital map
pmap = partialize(map)

# Discard everything
def void(*_, **__):
    pass

# Map that directly evaluate the generator and discard the result
def dump_map(fn, *args):
    void(*map(fn, *args))

# Will evaluate a function
def apply(fn):
    return fn()

# Iter on callable
def map_apply(iters):
    return map(apply, iters)


decor_and_wraps = lambda fn, *decos: fc.compose(ft.wraps(fn), *decos)

@ft.wraps(cu.cached)
def cached(cache, scoped=True, typed=False, key=None):
    return lambda fn : decor_and_wraps(fn,
        cu.cached(cache, scoped, typed, key))(fn) 

def partialize_cached(cache, scoped=True, typed=False, key=None):
    return fc.compose(partialize, cached(cache, scoped, typed, key)) 

def pcompose(*funs):
    return partialize(fc.compose(*funs))

def prcompose(*funs):
    return partialize(fc.rcompose(*funs))

def cached_pcompose(cache, *funs):
    return partialize_cached(cache)(fc.compose(*funs)) 

def cached_prcompose(cache, *funs):
    return partialize_cached(cache)(fc.rcompose(*funs)) 

# def cached_compose(cache, *funs):
#     @cached(cache)
#     def compose_apply(*args):
#             return fc.compose(*funs)(*args)
#     return compose_apply

# def cached_rcompose(cache, *funs):
#     @cached(cache)
#     def rcompose_apply(*args):
#             return fc.rcompose(*funs)(*args)
#     return rcompose_apply


@partialize
def print_forward(comment, x):
    print(comment, x)
    return x

@partialize
def get(key, seq):
    return seq[key]

@partialize
def equal_to(arg1, arg2):
    return arg1 == arg2

first_filter = partialize(fc.compose(fc.first, fc.filter))
all_filter = partialize(fc.compose(fc.all, fc.filter))

@partialize
def select_values(key, seq):
    return {s[key] for s in seq}

# @partialize
# def find_pos(value, seq):
#     return list(seq).index(value)

def field_match(key, value):
    return fc.compose(equal_to(value), get(key))

def match_at(value, pos):
    return fc.compose(equal_to(value), get(pos))

def evaluate(fn): return fn()



file_data_cache = cu.LRU(max_size=128)

@decor_and_wraps(json.load, cached(file_data_cache))
def json_load(filename):
    print("Loading JSON file :{}".format(filename))
    return json.load(open(filename))

@cached(file_data_cache)
def csv_load(filename):
    print("Loading CSV file :{}".format(filename))
    return csv.reader(open(filename))

file_loader = {
    '.json' : json_load,
    '.csv' : csv_load}

def file_load(filename):
    return file_loader[Path(filename).ext](filename)


# json_find_bench_by_name = lambda name : fc.rcompose(get("benchmarks"), first_filter(field_match("name", name)))

# csv_find_bench_by_name = lambda name : first_filter(match_at(name, 0))

prop_cache = cu.LRU(max_size=2048)

def flat_iter(*iters):
    '''Generate an unique iterator that iterate through all
    iters given as parameter'''
    for ite in iters:
        for e in ite:
            yield e

def concat(*datas, dim=None):
    return xr.concat(list(datas), dim=dim)
    # return xr.concat(xr.broadcast(flat_iter(*datas)), dim=dim)

merge = fc.partial(ft.reduce, operator.or_)

dict_zip = compose(dict, zip)

# def load_function_list(commit):
#     data = json_load("{}/data.json".format(commit))


# def benchs_of(json_data):
#     return cached_rcompose(prop_cache, )


dims = ('commit', 'function', 'bench')

zip_dims = fc.partial(dict_zip, dims)

base_directory = Path('data')

commit_list_file = Path('commit.json')
commit_data_file = Path('data.json')

def lazy(fn, *args, **kwargs):
    return fc.partial(fn, *args, **kwargs)

def commit_data(commit):
    return file_load(base_directory / commit / commit_data_file)

commit_list = lazy(file_load, base_directory / commit_list_file)

get_function_list = get('properties')
get_bench_list = get('bench')

get_function_name = get('test')
get_bench_name = get('type')

get_function_count = len

find_function_by_name = lambda function_name : first_filter(field_match('test', function_name))


# Take commit id
function_list_of = rcompose(commit_data, get_function_list)

def toto(commit, f):
    benchs = get_bench_list(f)
    f_name = get_function_name(f)

    print('Bench of {} {} : {}'.format(commit, f_name, list(map(get_bench_name, benchs))))
    coords = zip_dims([[commit], [str(f_name)], list(map(compose(str, get_bench_name), benchs))])
    data = xr.DataArray(np.array(list(map(len, benchs))).reshape(1, 1, len(benchs)),
        dims=dims, coords=coords)
    print(data)
    return data


def get_data(commit):
    functions = function_list_of(commit)
    print('Function : {}'.format(set(map(get_function_name, functions))))

    return ft.reduce(fc.partial(concat, dim=dims[0]), map(lazy(toto, commit), functions))



    # for f in functions:
    #     benchs = get_bench_list(f)
    #     f_name = get_function_name(f)
    #     print('Bench of {} : {}'.format(f_name, list(map(get_bench_name, benchs))))
    #     data = xr.DataArray(np.array(benchs).reshape(1, 1, len(benchs))),
    #         dims=dims, coords=zip_dims([commit, f_name, list(map(get_bench_name, benchs)))



    # return xr.DataArray()

# class Anal:
#     def __init__(self):
#         self.commit_list = commit_list()


#     def append()


























# Take commit id and function id
# def bench_list_of(commit, function):
#         return fc.rcompose(
#             function_list_of(commit),
#             find_function_by_name(function),
#             get_bench_list)()

# Take commit id and function id
# @partialize
# def bench_list_of(commit, function):
#         return fc.rcompose(
#             function_list_of(commit),
#             find_function_by_name(function),
#             get_bench_list)()

# function_name_list_of = prcompose(
#     function_list_of, apply,
#     pmap(get_function_name))

# bench_name_list_of = prcompose(
#     bench_list_of, apply,
#     pmap(get_bench_name))






















# @np.vectorize
# def evaluate(fn):
#     return fn()

# evaluate = np.vectorize(lambda fn: fn(), otypes=[object])


# regular_google = {
#         'mean' : get('real_time'),
#         'bench' : json_find_bench_by_name
# }

# regular_granite = {
#         'mean' : fc.rcompose(get(2), float, int),
#         'bench': csv_find_bench_by_name

# }

# regular_bench = {
#         'google'  : regular_google,
#         'granite' : regular_granite
# }

# runtime_granite = {
#         'raw' : fc.identity,
#         'bench' : lambda name, data : data 
# }

# runtime_bench = {
#         'granite' : runtime_granite
# }

# benchmarks = {
#         'regular' : regular_bench,
#         'runtime' : runtime_bench
# }


# jdata = json_load("data/fun1_reg.json")
# cdata = csv_load("data/fun2_reg.csv")


# fun1_jbench = cached_rcompose(prop_cache, jdata,
#         json_find_bench_by_name("BM_Fun1"))

# fun1_mean = cached_rcompose(prop_cache, fun1_jbench,
#         regular_google['mean'])

# # fun1_rep = cached_rcompose(prop_cache, fun1_jbench,
# #         get("repetitions"), print_forward('get repetitions'))



# fun2_cbench = cached_rcompose(prop_cache, cdata,
#         csv_find_bench_by_name("BM_Fun2"))

# fun2_mean = cached_rcompose(prop_cache, fun2_cbench,
#         regular_granite['mean'])

# fun2_cpu = cached_rcompose(prop_cache, fun2_cbench,
#         get(3), float, int)
