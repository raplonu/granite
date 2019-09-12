import functools as ft
import funcy as fc
from funcy import partial, compose, rcompose
import itertools
from path import Path

import  boltons.cacheutils as cu
from cachetools.keys import hashkey

import json
import csv

import numpy  as np
import pandas as pd
# import xarray as xr

import matplotlib.pyplot as plt

import statistics
from sklearn.linear_model import LinearRegression

import operator

import sqlite3

from pampy import match, _

plt.ion()

from meta import *

'''
   `7MMF' .g8""8q. `7MM"""Yp,
     MM .dP'    `YM. MM    Yb
     MM dM'      `MM MM    dP
     MM MM        MM MM"""bg.
     MM MM.      ,MP MM    `Y
(O)  MM `Mb.    ,dP' MM    ,9
 Ymmm9    `"bmmd"' .JMMmmmd9
'''

### File functions

def read_file(filename):
    print("Loading file : {}".format(filename))
    return open(filename).read()

def json_load(filename):
    print("Loading JSON file : {}".format(filename))
    return json.load(open(filename))

def csv_load(filename):
    print("Loading CSV file : {}".format(filename))
    return list(csv.reader(open(filename)))

file_loader = {
    '.json' : json_load,
    '.csv' : csv_load}

def file_load(filename):
    return at(extension(filename), file_loader, default=read_file)(filename)

def concat(*datas, dim=None):
    return xr.concat(list(datas), dim=dim)
    # return xr.concat(xr.broadcast(flat_iter(*datas)), dim=dim)

dims = ('commit', 'function', 'prop')

def bench_array(data, dims, coords):
    return xr.DataArray(np.array(data).reshape(1, 1, len(data)), dims=dims, coords=coords)

properties = ['mean', 'min', 'max', 'jitter', 'scale']

'''
`7MM"""YMM  `7MN.   `7MF'`7MMF'  `7MMF'      db      `7MN.   `7MF' .g8"""bgd `7MM"""YMM  `7MM"""Yb.
  MM    `7    MMN.    M    MM      MM       ;MM:       MMN.    M .dP'     `M   MM    `7    MM    `Yb.
  MM   d      M YMb   M    MM      MM      ,V^MM.      M YMb   M dM'       `   MM   d      MM     `Mb
  MMmmMM      M  `MN. M    MMmmmmmmMM     ,M  `MM      M  `MN. M MM            MMmmMM      MM      MM
  MM   Y  ,   M   `MM.M    MM      MM     AbmmmqMA     M   `MM.M MM.           MM   Y  ,   MM     ,MP
  MM     ,M   M     YMM    MM      MM    A'     VML    M     YMM `Mb.     ,'   MM     ,M   MM    ,dP'
.JMMmmmmMMM .JML.    YM  .JMML.  .JMML..AMA.   .AMMA..JML.    YM   `"bmmmd'  .JMMmmmmMMM .JMMmmmdP'
'''

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

@boost_fn
def get_range(range_name):
    cursor.execute('''
    SELECT name FROM {}'''.format(range_name))
    return map_to_list(fc.first, cursor.fetchall())

range_names = call_once(get_range, 'dimensions')

get_all_ranges = (map_to_list << get_range) * range_names

def handle_str(data):
    print('handle_str with {}'.format(data))
    return eval(data)

@boost_fn
def match_value(value):
    return match(value,
        Path, match_value * file_load,
        str, match_value * handle_str,
        dict, 42,
        list, tuple,
        _, fwd
    )

eval_match = match_value * eval

@boost_fn
def get_data(dims):
    cursor.execute('''
    SELECT * FROM data_view''')
    return pd.DataFrame(cursor.fetchall(), columns=range_names()+['values'])

print('Hello, welcome to ...')
print('''
   ____   ,---.   .--.  ____     .---.       ____     __ .-'\''-.     .-''-. .-------.
 .'  __ `.|    \  |  |.'  __ `.  | ,_|       \   \   /  / _     \  .'_ _   \|  _ _   \
/   '  \  \  ,  \ |  /   '  \  ,-./  )        \  _. /  (`' )/`--' / ( ` )   ' ( ' )  |
|___|  /  |  |\_ \|  |___|  /  \  '_ '`)       _( )_ .(_ o _).   . (_ o _)  |(_ o _) /
   _.-`   |  _( )_\  |  _.-`   |> (_)  )   ___(_ o _)' (_,_). '. |  (_,_)___| (_,_).' __
.'   _    | (_ o _)  .'   _    (  .  .-'  |   |(_,_)' .---.  \  :'  \   .---|  |\ \  |  |
|  _( )_  |  (_,_)\  |  _( )_  |`-'`-'|___|   `-'  /  \    `-'  | \  `-'    /  | \ `'   /
\ (_ o _) /  |    |  \ (_ o _) / |        \       /    \       /   \       /|  |  \    /
 '.(_,_).''--'    '--''.(_,_).'  `--------` `-..-'      `-...-'     `'-..-' ''-'   `'-'

''')


















# def super_toto(iterators, names):
#     pass

# class commit_obj:
#     def __init__(self, path):
#         self.path = path

#     def __repr__(self):
#         return self.path

# def commit_range(path):
#     path = Path(path)
#     return map(
#         bf(commit_obj) * (bf(operator.truediv) << path),
#         b_file_load(path / 'commit.json'))

# class function_obj:
#     def __init__(self, path, data):
#         self.path = path
#         self.data = data

#     def __repr__(self):
#         return '{} at {}'.format(self.data['test'], self.path)


# def function_range(commit):
#     return map(
#         bf(function_obj) << Path(commit),
#         at('properties', b_file_load(Path(commit) / 'data.json')))

# class bench_obj:
#     def __init__(self, path, data):
#         self.__path = path
#         self.__data = data

#     @property
#     def path(self):
#         return self.__path

#     @property
#     def data(self):
#         return self.__data

# def bench_range(function):
#     return map(bf(bench_obj) << function.path, at('bench', function.data))

# class attribute_obj:
#     def __init__(self):
#         pass

# def bench_to_attributes(bench):
#     result = {}
#     accessors = explore(keys_of(bench), me_dict)
#     for k, e in accessors.items():
#         result[k] = call_once(bf(e(bench)) * file_bench)
#     return result







# file_data_cache = cu.LRU(max_size=128)

# b_file_load = boost_fn(cached(file_data_cache)(file_load))

# base_directory = Path('data')
# commits_filename = Path('commit.json')
# commit_data_filename = Path('data.json')

# # Unit -> list commit_id
# # List of commits, lazy access
# commits = lazy(b_file_load, base_directory / commits_filename)

# commit_path = lambda commit : base_directory / commit

# # commit_id -> Path
# # Get file path of a specific commit
# @boost_fn
# def commit_data_path(commit):
#     return base_directory / commit / commit_data_filename
# @boost_fn
# def bench_data_path(commit, bench):
#     return base_directory / commit / at('file', bench)

# # commit_id -> dict
# # Get data of a specific commit
# commit_data = b_file_load * commit_data_path

# get_function_list = at << 'properties'
# get_bench_list = at << 'bench'

# get_function_name = at << 'test'
# get_bench_name = at << 'type'

# at_bench_name = at << 'bench_name'

# get_function_count = b_len

# # Take commit id
# function_list_of = get_function_list * commit_data


# data_cache = cu.LRU(max_size=2048)


# zip_dims_with = b_partial(zip_to_dict, dims) * pack





# def reduce_concat(xarrays, dim):
#     '''
#     Concat a sequence of xarray on selected dim
#     '''
#     return ft.reduce(partial(concat, dim=dim), xarrays)


# @boost_fn
# def regular_google_json_mean(bench):
#     return (at << 'benchmarks') | \
#            (first_filter << field_match('name', at_bench_name(bench))) | \
#            (at << 'real_time')

# @boost_fn
# def runtime_granite_csv_mean( _ ):
#     return bf(np.mean) * partial(np.array, dtype=float)

# regular_google_csv_header_line = 9

# find_realtime_index = lambda data : find_pos('real_time', data[regular_google_csv_header_line])
# select_data_field_by_name = lambda bench : first_filter << field_match(0, at_bench_name(bench))

# @boost_fn
# def regular_google_csv_mean( bench ):
#     return lambda data : ((at << find_realtime_index(data)) * \
#                          select_data_field_by_name(bench))(data)

# def bench_data_at(bench):
#     return b_file_load(bench.path / bench.data['file'])

# me_dict = {
#     'regular' : {
#         'google' : {
#             '.json' : {
#                 'mean' : (regular_google_json_mean * bench_data_at)},
#             '.csv' : {
#                 'mean' : (regular_google_csv_mean * bench_data_at)}}},
#     'runtime' : {
#         'granite' : {
#             '.csv' : {
#                 'run' : (runtime_granite_csv_mean * bench_data_at)}}},
#     'scale' : {
#         'granite' : {
#             '.json' : {
#                 'scale' : (regular_google_json_mean * bench_data_at)}}}}

# bench_type = at << 'type'
# bench_generator = at << 'generator'
# bench_ext = extension * (at << 'file')



# def keys_of(bench):
#     return map(apply << bench, (bench_type, bench_generator, bench_ext))

# def compute_props(benchs, bench_to_path):
#     result = {}
#     for bench in benchs:
#         accessors = explore(keys_of(bench), me_dict)
#         file_bench = b_file_load * (bench_to_path << bench)
#         for accessor in accessors.items():
#             result[accessor[0]] = call_once(bf(accessor[1](bench)) * file_bench)

#     return result

# @boost_fn
# def get_benchs(commit, function):
#     benchs = get_bench_list(function)

#     print('Process {} {}'.format(commit, get_function_name(function)))

#     properties = compute_props(benchs, bench_data_path << commit)

#     coords = zip_dims_with(
#         [commit],
#         [get_function_name(function)],
#         list(properties.keys()))

#     return bench_array(list(properties.values()), dims, coords)


# def get_data(commit):
#     return reduce_concat(
#         map(get_benchs << commit, function_list_of(commit)),
#         dims[1])


# def get_all_data():
#     return reduce_concat(
#         map(get_data, commits()),
#         dims[0])

# @np.vectorize
# def invoke_element(e):
#     return e() if callable(e) else e

# @boost_fn
# def transform(fn, data):
#     fn = np.vectorize(fn)
#     return xr.apply_ufunc(lambda e : fn(e), data)

# transform_invoke = transform << invoke_element






# def partialize(fn):
#     @boost_fn
#     def partialize_impl(*args, **kwargs):
#         return b_partial(*args, **kwargs)
#     return partialize_impl

# @fc.decorator
# def partialize(fn):
#     return boost_fn(partial(fn))

# Parital map
# pmap = partialize(map)




# # Discard everything
# @boost_fn
# def void(*_, **__):
#     pass

# # Map that directly evaluate the generator and discard the result
# @boost_fn
# def dump_map(fn, *args):
#     void(*map(fn, *args))

# list_map = b_list * b_map


# decor_and_wraps = lambda fn, *decos: compose(ft.wraps(fn), *decos)



# @ft.wraps(cu.cached)
# def cached(cache, scoped=True, typed=False, key=None):
#     return lambda fn : decor_and_wraps(fn,
#         cu.cached(cache, scoped, typed, key))(fn)


# def partialize_cached(cache, scoped=True, typed=False, key=None):
#     return fc.compose(partialize, cached(cache, scoped, typed, key))

# def pcompose(*funs):
#     return partialize(compose(*funs))

# def prcompose(*funs):
#     return partialize(rcompose(*funs))

# def cached_pcompose(cache, *funs):
#     return partialize_cached(cache)(compose(*funs))

# def cached_prcompose(cache, *funs):
#     return partialize_cached(cache)(rcompose(*funs))

# @partialize
# def print_forward(comment, x):
#     print(comment, x)
#     return x

# @partialize
# def get(key, seq):
#     return seq[key]

# @partialize
# def equal_to(arg1, arg2):
#     return arg1 == arg2

# first_filter = partialize(fc.compose(fc.first, fc.filter))
# all_filter = partialize(fc.compose(fc.all, fc.filter))

# @partialize
# def select_values(key, seq):
#     return {s[key] for s in seq}

# # @partialize
# # def find_pos(value, seq):
# #     return list(seq).index(value)

# def field_match(key, value):
#     return fc.compose(equal_to(value), get(key))

# def match_at(value, pos):
#     return fc.compose(equal_to(value), get(pos))

# def evaluate(fn): return fn()



# prop_cache = cu.LRU(max_size=2048)

# def flat_iter(*iters):
#     '''Generate an unique iterator that iterate through all
#     iters given as parameter'''
#     for ite in iters:
#         for e in ite:
#             yield e

# @partialize
# def concat(*datas, dim=None):
#     return xr.concat(list(datas), dim=dim)
#     # return xr.concat(xr.broadcast(flat_iter(*datas)), dim=dim)

# merge = fc.partial(ft.reduce, operator.or_)

# dict_zip = compose(dict, zip)





# zip_dims = compose(fc.partial(dict_zip, dims), pack)

# def lazy(fn, *args, **kwargs):
#     return fc.partial(fn, *args, **kwargs)

# def commit_data(commit):
#     return file_load(base_directory / commit / commit_data_file)

# get_function_list = get('properties')
# get_bench_list = get('bench')

# get_function_name = get('test')
# get_bench_name = get('type')

# get_function_count = len

# find_function_by_name = lambda function_name : first_filter(field_match('test', function_name))


# properties = ['mean', 'min', 'max', 'jitter', 'scale']


# def get_google_json_mean(path, data):
#     return rcompose(get('benchmarks'), first_filter(field_match('name', get('bench_name')(bench))), get('real_time'))

# def get_granite_csv_mean(path, data):
#     return np.mean(list_map(compose(float, get(0)), data))


# bench_path = lambda commit, bench : base_directory / commit / get('file')(bench)


# def get_mean(commit, function, benchs):
#     regular_bench = first_filter(field_match('type', 'regular'))(benchs)

#     path = bench_path(commit, regular_bench)

#     data = file_load(path)

# def compute_props(commit_id, function_id, benchs):
#     for bench in benchs:
#         pass







# # Take commit id
# function_list_of = rcompose(commit_data, get_function_list)


# # def plot_data(xarr):
# #     pan = xarr.to_pandas()
# #     pan.plot() if pan.dtype is not np.dtype(object) else dump_map(plt.plot, pan)


# def bench_array(data, dims, coords):
#     return xr.DataArray(np.array(data).reshape(1, 1, len(data)), dims=dims, coords=coords)

# def compute_props(commit_id, function_id, benchs):
#     for bench in benchs:
#         pass

# @partialize
# def get_benchs(commit, f):
#     benchs = get_bench_list(f)

#     print('Commit at {} {} : {}'.format(commit, get_function_name(f), benchs))

#     # properties = compute_props(commit, get_function_name(f), benchs)

#     coords = zip_dims(
#         [commit],
#         [get_function_name(f)],
#         list(map(get_bench_name, benchs)))

#     return bench_array(benchs, dims, coords)




# def get_data(commit):
#     return ft.reduce(
#         concat(dim=dims[1]),
#         map(get_benchs(commit), function_list_of(commit)))


# def get_all_data():
#     return ft.reduce(
#         concat(dim=dims[0]),
#         map(get_data, commit_list()))















# def data_of(data_f, data_list, dim_id):
#     return ft.reduce(
#         concat(dim=dims[dim_id]),
#         map(data_f, data_list))

# get_commit_data = lambda commit : data_of(get_benchs(commit), function_list_of(commit), 1)

# get_all_data = data_of(get_commit_data, commit_list(), 0)




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
