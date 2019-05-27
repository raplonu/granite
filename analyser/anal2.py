import json
import statistics
from functools import partial
import numpy as np
from sklearn.linear_model import LinearRegression
import operator

dump_map = lambda func, *args : (lambda *args : None)(*map(func, *args))

def constant_function(value):
    return lambda : value