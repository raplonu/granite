import functools as ft
import funcy as fc
from funcy import partial, compose, rcompose
import itertools
from path import Path

import  boltons.cacheutils as cu
from cachetools.keys import hashkey

import operator

from pampy import match, _

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

def rpartial(fun, *args2, **kwargs2):
    def rpartial_impl(*args1, **kwargs1):
        return fun(*args1, *args2, **kwargs1, **kwargs2)
    return rpartial_impl

class Function:
    def __init__(self, fn):
        self.__fn = fn

    def __call__(self, *args, **kwargs):
        return self.__fn(*args, **kwargs)

    def __mul__(self, ofn):
        return Function(compose(self.__fn, Function.filter_fn(ofn)))

    def __or__(self, ofn):
        return Function(rcompose(self.__fn, Function.filter_fn(ofn)))

    def __lshift__(self, arg):
        return Function(partial(self.__fn, arg))

    def __rshift__(self, arg):
        return Function(rpartial(self.__fn, arg))

    @staticmethod
    def filter_fn(fn):
        return fn.__fn if isinstance(fn, Function) else fn

    def partial(self, *args, **kwargs):
        return Function(partial(self.__fn, *args, **kwargs))

    def rpartial(self, *args, **kwargs):
        return Function(rpartial(self.__fn, *args, **kwargs))

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
b_range = boost_fn(range)
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
def at(key, seq, default=None):
    return seq[key] if key in seq else default

@boost_fn
def get(seq, pos, default=None):
    return seq[pos] if pos < len(seq) else default


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

@boost_fn
def flat_map(range_, generator):
    for r in range_:
        for e in generator(r):
            yield e



def compose_gens(*gens):
    return lambda data :\
        ft.reduce(flat_map, [[data], *gens[::-1]])

@boost_fn
def filename(path):
    return Path(path).name

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

@boost_fn
def fwd(x):
    return x

@boost_fn
def not_none_fwd_or(arg, fallback):
    return arg if arg is not None else fallback
