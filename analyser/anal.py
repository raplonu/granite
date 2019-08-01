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
import xarray as xr

import matplotlib.pyplot as plt

import statistics
from sklearn.linear_model import LinearRegression

import operator

plt.ion()

'''                                                        
MMP""MM""YMM   .g8""8q.     .g8""8q. `7MMF'       .M"""bgd 
P'   MM   `7 .dP'    `YM. .dP'    `YM. MM        ,MI    "Y 
     MM      dM'      `MM dM'      `MM MM        `MMb.     
     MM      MM        MM MM        MM MM          `YMMNq. 
     MM      MM.      ,MP MM.      ,MP MM      , .     `MM 
     MM      `Mb.    ,dP' `Mb.    ,dP' MM     ,M Mb     dM 
   .JMML.      `"bmmd"'     `"bmmd"' .JMMmmmmMMM P"Ybmmd"  
'''

class MeCachedFunction(cu.CachedFunction):
    def __call__(self, *args, **kwargs):
        cache = self.get_cache()
        arg = [self.func, *args] if self.scoped else args
        key = self.key_func(arg, kwargs, typed=self.typed)
        if key in cache:
            return cache[key]
        else:
            ret = cache[key] = self.func(*args, **kwargs)
            return ret

@ft.wraps(cu.cached)
def cached(cache, scoped=True, typed=False, key=None):
    def cached_func_decorator(func):
        return MeCachedFunction(func, cache, scoped=scoped, typed=typed, key=key)
    return cached_func_decorator



def compose_doc(obj1, obj2):
    if obj1.__doc__ is None:
        return obj2.__doc__
    elif obj2.__doc__ is not None:
        return obj1.__doc__ + '\n\n' + obj2.__doc__
    return None

class Function:
    def __init__(self, fn, doc = None):
        self.__fn = fn
        self.__doc__ = doc if doc is not None else fn.__doc__

    def __call__(self, *args, **kwargs):
        return self.__fn(*args, **kwargs)

    def __mul__(self, ofn):
        return Function(compose(self.__fn, Function.filter_fn(ofn)), compose_doc(ofn, self))

    def __or__(self, ofn):
        return Function(rcompose(self.__fn, Function.filter_fn(ofn)), compose_doc(self, ofn))

    def __lshift__(self, arg):
        return Function(partial(self.__fn, arg), self.__doc__)

    @staticmethod
    def filter_fn(fn):
        return fn.__fn if isinstance(fn, Function) else fn

    # def partial(self, *args, **kwargs):
    #     return Function(partial(self.__fn, *args, **kwargs), self.__doc__)

    # @property
    # def map(self):
    #     return Function(partial(map, self.__fn), compose_doc(map, self))

    # def cached(self, cache, scoped=True, typed=False):
    #     print('@@@@ ', self.__fn.__str__)
    #     return Function(cu.cached(cache, key=partial(hashkey, self.__fn.__str__))(self.__fn), self.__doc__)

    # def map(self, *args):
    #     return Function(partial(map, self.__fn, *args), map + '\n\n' + self.__doc__)

# @fc.decorator
def boost_fn(fn):
    return Function(fn)

# Alias of boost_fn
bf = boost_fn

b_len = boost_fn(len)
b_map = boost_fn(map)
b_zip = boost_fn(zip)
b_list = boost_fn(list)
b_set = boost_fn(set)
b_dict = boost_fn(dict)
b_str = boost_fn(str)
b_float = boost_fn(float)
b_int = boost_fn(int)

# Discard everything
@boost_fn
def void(*_, **__):
    pass

# Map that directly evaluate the generator and discard the result
@boost_fn
def dump_map(fn, *args):
    void(*map(fn, *args))
        # self.__doc__ = doc if doc is not None else fn.__doc__

@boost_fn
def b_partial(fn, *args1, **kwargs1):
    @boost_fn
    def b_partial_impl(*args2, **kwargs2):
        return fn(*args1, *args2, **kwargs1, **kwargs2)
    return b_partial_impl

@fc.decorator
def partialize(fn):
    @boost_fn
    def partialize_impl(*args, **kwargs):
        return b_partial(*args, **kwargs)
    return partialize_impl


lazy = partial

@boost_fn
def at(key, seq):
    return seq[key]

@boost_fn
def equal_to(arg1, arg2):
    return arg1 == arg2

first_filter = boost_fn(compose(fc.first, fc.filter))
all_filter   = boost_fn(compose(fc.all,   fc.filter))

# @partialize
# def select_values(key, seq):
#     return {s[key] for s in seq}

@boost_fn
def find_pos(value, seq):
    return list(seq).index(value)

@boost_fn
def field_match(key, value):
    return (equal_to << value) * (at << key)

# @boost_fn
# def match_at(value, pos):
#     return (equal_to << value) * (at << pos)

@boost_fn
def pack(*args):
    return args

zip_to_dict = b_dict * b_zip
map_to_list = b_list * b_map

# @boost_fn
# def flat_iter(*iters):
#     '''Generate an unique iterator that iterate through all
#     iters given as parameter'''
#     for ite in iters:
#         for e in ite:
#             yield e

@boost_fn
def extension(path):
    return Path(path).ext

@boost_fn
def explore(keys, data):
    return ft.reduce(operator.getitem, keys, data)

@boost_fn
def apply(*args, **kwargs):
    '''
    A function that will store arguments and use the last one as a function that will be call

    '''
    *args, fn = args
    return fn(*args, **kwargs)

@boost_fn
def call_once(fn, *args, **kwargs):
    fn = partial(fn, *args, **kwargs)
    @boost_fn
    def call_once_impl():
        if not hasattr(call_once_impl, 'result'):
            call_once_impl.result = fn()
        return call_once_impl.result
    return call_once_impl

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
    return file_loader[extension(filename)](filename)

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


# iter = element, category name, repre


class commit_file:
    def __init__(self, path):
        self.path = Path(path)

    def __repr__(self):
        return self.path.name

class commit_iterator:
    def __init__(self, path):
        # Path to commit.json
        self.path = Path(path)

    def __iter__(self):
        return map(lambda commit: commit_file(self.path.dirname() / commit), b_file_load(self.path))

    def __repr__(self):
        return 'commits at {}'.format(self.path)


class commits_obj:
    def __init__(self, path):
        self.__path = Path(path)
    
    @property
    def path(self):
        return self.__path / 'commit.json'

    @property
    def dirname(self):
        return self.__path

    @property
    def category(self):
        return 'commit'

    def __repr__(self):
        return 'Commits at {}'.format(self.path)

class functions_obj:
    def __init__(self, path):
        self.__path = Path(path)

    @property
    def path(self):
        return self.__path / 'data.json'

    @property
    def category(self):
        return 'function'

    def __repr__(self):
        return 'Functions at {}'.format(self.__path)


class benchs_obj:
    def __init__(self, data):
        self.__data = data

    @property
    def data(self):
        return self.__data

    @property
    def category(self):
        return 'bench'

    def __repr__(self):
        return 'Benchs of {}'.format(self.data['test'])



# input 'data'
# output ['data/23ef', 'data/98ab']
def fun1(co):
    print('Handle {}'.format(co))
    return map(lambda commit: co.dirname / commit, b_file_load(co.path))


# input 'data/23ef'
# output [{...}, {...}]
def fun2(fo):
    print('Handle {}'.format(fo))
    return b_file_load(fo.path)['properties']

def fun3(bo):
    return bo.data['bench']



# class function_iterator:
#     def __init__


# class me_iter:
#     def __init__(self, it, category_name, rep):
#         self.it = it
#         self.category_name = category_name

#     def __repr__(self):
#         return self._repr






file_data_cache = cu.LRU(max_size=128)

b_file_load = boost_fn(cached(file_data_cache)(file_load))

base_directory = Path('data')
commits_filename = Path('commit.json')
commit_data_filename = Path('data.json')

# Unit -> list commit_id
# List of commits, lazy access
commits = lazy(b_file_load, base_directory / commits_filename)

commit_path = lambda commit : base_directory / commit

# commit_id -> Path
# Get file path of a specific commit
@boost_fn
def commit_data_path(commit):
    return base_directory / commit / commit_data_filename
@boost_fn
def bench_data_path(commit, bench):
    return base_directory / commit / at('file', bench)

# commit_id -> dict
# Get data of a specific commit
commit_data = b_file_load * commit_data_path

get_function_list = at << 'properties'
get_bench_list = at << 'bench'

get_function_name = at << 'test'
get_bench_name = at << 'type'

at_bench_name = at << 'bench_name'

get_function_count = b_len

# Take commit id
function_list_of = get_function_list * commit_data


data_cache = cu.LRU(max_size=2048)


zip_dims_with = b_partial(zip_to_dict, dims) * pack





def reduce_concat(xarrays, dim):
    '''
    Concat a sequence of xarray on selected dim
    '''
    return ft.reduce(partial(concat, dim=dim), xarrays)


def regular_google_json_mean(bench):
    return (at << 'benchmarks') | \
           (first_filter << field_match('name', at_bench_name(bench))) | \
           (at << 'real_time')

def runtime_granite_csv_mean( _ ):
    return bf(np.mean) * partial(np.array, dtype=float)

regular_google_csv_header_line = 9

find_realtime_index = lambda data : find_pos('real_time', data[regular_google_csv_header_line])
select_data_field_by_name = lambda bench : first_filter << field_match(0, at_bench_name(bench))

def regular_google_csv_mean( bench ):
    return lambda data : ((at << find_realtime_index(data)) * \
                         select_data_field_by_name(bench))(data)

me_dict = {
    'regular' : {
        'google' : {
            '.json' : {
                'mean' : regular_google_json_mean},
            '.csv' : {
                'mean' : regular_google_csv_mean}}},
    'runtime' : {
        'granite' : {
            '.csv' : {
                'run' : runtime_granite_csv_mean}}},
    'scale' : {
        'granite' : {
            '.json' : {
                'scale' : regular_google_json_mean}}}}

bench_type = at << 'type'
bench_generator = at << 'generator'
bench_ext = extension * (at << 'file')



def keys_of(bench):
    return map(apply << bench, (bench_type, bench_generator, bench_ext))

def compute_props(benchs, bench_to_path):
    result = {}
    for bench in benchs:
        accessors = explore(keys_of(bench), me_dict)
        file_bench = b_file_load * (bench_to_path << bench)
        for accessor in accessors.items():
            result[accessor[0]] = call_once(bf(accessor[1](bench)) * file_bench) 

    return result

@boost_fn
def get_benchs(commit, function):
    benchs = get_bench_list(function)

    print('Process {} {}'.format(commit, get_function_name(function)))

    properties = compute_props(benchs, bench_data_path << commit)

    coords = zip_dims_with(
        [commit],
        [get_function_name(function)],
        list(properties.keys()))

    return bench_array(list(properties.values()), dims, coords)


def get_data(commit):
    return reduce_concat(
        map(get_benchs << commit, function_list_of(commit)),
        dims[1])


def get_all_data():
    return reduce_concat(
        map(get_data, commits()),
        dims[0])

@np.vectorize
def invoke_element(e):
    return e() if callable(e) else e

@boost_fn
def transform(fn, data):
    fn = np.vectorize(fn)
    return xr.apply_ufunc(lambda e : fn(e), data)

transform_invoke = transform << invoke_element

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
