import functools as ft
import funcy as fc
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
all_filter = partialize(fc.compose(fc.all, fc.filter))

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

def evaluate(fn): return fn()



file_data_cache = cu.LRU(max_size=128)

@decor_and_wraps(json.load, partialize_cached(file_data_cache))
def json_load(filename):
    print("Loading JSON file :{}".format(filename))
    return json.load(open(filename))

@partialize_cached(file_data_cache)
def csv_load(filename):
    print("Loading CSV file :{}".format(filename))
    return csv.reader(open(filename))

file_loader = {
    '.json' : json_load,
    '.csv' : csv_load}

def file_load(filename):
    return file_loader[Path(filename).ext](filename)


json_find_bench_by_name = lambda name : fc.rcompose(get("benchmarks"), first_filter(field_match("name", name)))

csv_find_bench_by_name = lambda name : first_filter(match_at(name, 0))

prop_cache = cu.LRU(max_size=2048)

print("Hello, welcome to ...")
print('''
   ____    ,---.   .--.   ____      .---.       ____     __  .-'\''-.     .-''-.  .-------.     
 .'  __ `. |    \  |  | .'  __ `.   | ,_|       \   \   /  // _     \  .'_ _   \ |  _ _   \    
/   '  \  \|  ,  \ |  |/   '  \  \,-./  )        \  _. /  '(`' )/`--' / ( ` )   '| ( ' )  |    
|___|  /  ||  |\_ \|  ||___|  /  |\  '_ '`)       _( )_ .'(_ o _).   . (_ o _)  ||(_ o _) /    
   _.-`   ||  _( )_\  |   _.-`   | > (_)  )   ___(_ o _)'  (_,_). '. |  (_,_)___|| (_,_).' __  
.'   _    || (_ o _)  |.'   _    |(  .  .-'  |   |(_,_)'  .---.  \  :'  \   .---.|  |\ \  |  | 
|  _( )_  ||  (_,_)\  ||  _( )_  | `-'`-'|___|   `-'  /   \    `-'  | \  `-'    /|  | \ `'   / 
\ (_ o _) /|  |    |  |\ (_ o _) /  |        \\      /     \       /   \       / |  |  \    /  
 '.(_,_).' '--'    '--' '.(_,_).'   `--------` `-..-'       `-...-'     `'-..-'  ''-'   `'-'   
                                                                                               
''')


def stick(*iters):
    '''Generate an unique iterator that iterate through all
    iters given as parameter'''
    for ite in iters:
        for e in ite:
            yield e


def concat(*datas, dim=None):
    return xr.concat(stick(*datas))

# def load_commit_list():#nmax = 100):
#     '''
#     if nmax = None -> load everything
#     '''
#     # if nmax < 0 : nmax = None

#     # Open file, read content and parse it as json

#     str_data = open("data/commit.json").read()
#     data = json.loads(str_data)
    
#     # select required data slice
#     # If nmax > len(data), the range will stop at len(data)
#     return file_load(data/commit.json) #[:nmax]














# def load_function_list(commit):
#     data = json_load("{}/data.json".format(commit))


# def benchs_of(json_data):
#     return cached_rcompose(prop_cache, )


dims = ('commit', 'function', 'bench')


base_directory = Path('data')
list_file = Path('commit.json')
data_file = Path('data.json')

commit_list = file_load(base_directory / list_file)

load_data_file = lambda commit: file_load(base_directory / commit / data_file)

function_list = lambda commit : cached_rcompose(prop_cache,
    load_data_file(commit),
    get('properties'),
    select_values('test'))



f_list = function_list(e) for e in commit_list()]


# jdata = lambda commit: json_load(base_directory / commit / commit_data)






# functions = [cached_rcompose(prop_cache,
#                 jdata(commit),
#                 get('properties'),
#                 select_values('test'))
#                 for commit in commit_list]



# data = None






# set_commit_list()


# def get_data()


























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
