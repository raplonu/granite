import json
import statistics
from functools import partial
import numpy as np
from sklearn.linear_model import LinearRegression
import operator

dump_map = lambda func, *args : (lambda *args : None)(*map(func, *args))

def addprop(clazz, name, fget=None, fset=None, fdel=None, doc=None):
    setattr(clazz, name, property(fget, fset, fdel, doc))

def get_get_f(name):
    return lambda obj, n=name: getattr(obj, n).get()

def get_set_f(name):
    return lambda obj, value, n=name: getattr(obj, n).set(value)

def get_del_f(name):
    return lambda obj, n=name: None #del(getattr(obj, n))

def privatename(name):
    return '_' + name

def gen_prop_f(name, doc=None):
    pname = privatename(name)
    return (name, get_get_f(pname), get_set_f(pname), get_del_f(pname))

def addproplistname(clazz, list_name):
    dump_map(lambda name : partial(addprop, clazz)(*gen_prop_f(name)), list_name)

class Node:
    def __init__(self, op = None, *sub):
        self.__op = op
        self.__sub = sub
        self.__con = []
        self.__has_value = False
        self.__sticky = False
        self.__value = None

        dump_map(lambda sub : sub.__subscribe(self), self.__sub)

    # @property
    def get(self):
        return self.__value

    # @value.setter
    def set(self, value):
        self.__set_value(value, True)

    def has_value(self):
        return self.__has_value

    def __subscribe(self, con):
        self.__con.append(con)

    def __set_value(self, value, sticky):
        self.__value = value
        self.__has_value = True
        self.__sticky = sticky
        self.__notify()


    def __try_update(self):
        if( not self
        and not self.__sticky
        and all(map(Node.has_value, self.__sub))
        ):
            self.__set_value(
                self.__op(*map(lambda n : n.get(), self.__sub)),
                False
            )
            self.__notify()

    def __notify(self):
        dump_map(Node.__try_update, self.__con)

    # def reset(self):
    #     if self and not self.__sticky :
    #         self.__value = None
    #         self.__has_value = False
    #         dump_map(Node.reset, self.__con)

    def __bool__(self):
        return self.has_value()



class basic_bench:
    def __init__(self):
        self._raw = Node()
        self._mean = Node(statistics.mean, self._raw)
        self._median = Node(statistics.median, self._raw)
        self._min = Node(min, self._raw)
        self._max = Node(max, self._raw)
        self._jitter = Node(operator.sub, self._max, self._min)
        self._stdev = Node(statistics.stdev, self._raw)

addproplistname(basic_bench, ["raw", "mean", "median", "min", "max", "jitter", "stdev"])





def compute_regression(data):
    x, y = data
    fit = LinearRegression().fit(x, y);
    return fit.coef_, fit.intercept_

class scale_bench:
    def __init__(self):
        self._raw = Node()
        self._regression = Node(compute_regression, self._raw)

addproplistname(scale_bench, ["raw", "regression"])



class runtime_bench:
    def __init__(self):
        self._raw = Node()
        self._regression = Node(compute_regression, self._raw)

addproplistname(runtime_bench, ["raw", "regression"])


class mega_bench:
    def __init__(self):
        self._basic = None
        self._linear = None




# class google_bench:
#     def mean(bench):
#         return bench["real_time"]

#     def name_match(bench, name):
#         return bench["name"] == name

#     def bench_by_name(benchs, name):
#         return next((bench for bench in benchs if google_bench.name_match(bench, name)), None)

#     def parse_bench(bench):
#         bb = basic_bench()
#         bb.mean = google_bench.mean(bench)

#         return bb

#     def benchs(jdata):
#         return jdata["benchmarks"]

#     def parse_names_bench(jdata, name):
#         return google_bench.parse_bench(google_bench.bench_by_name(google_bench.benchs(jdata), name))


# bench_map = {'granite' : google_bench, 'google' : google_bench}


# def load_benchs(jdata):
#     res = {}
#     for prop in jdata["properties"]:
#         res[prop["test"]] = [bench for bench in prop["bench"]]
#     return res





