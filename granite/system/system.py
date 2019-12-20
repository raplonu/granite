from granite.utils.functional import bf, apply, map_at_or_implace, flat_map, transpose, first
from granite.bench.bench_utils import process_container
from granite.command.commands import print_iter

import pandas as pd
import numpy as np

def init_data_frame(index, columns):
    idx = pd.MultiIndex(levels=[[]] * len(index),
            codes=[[]] * len(index),
            names=index)
    return pd.DataFrame(index=idx, columns=columns)

def exec_benchs(bench_callable):
    # Call every bench, separate keys and values then transpose the lists.

    l = list(map(transpose * dict.items * apply * first, bench_callable.values))

    columns, values = transpose(l)

    data = [pd.DataFrame(data=[v], columns=c) for c, v in zip(columns, values)]

    # Merge every result in a single DataFrame
    res = pd.concat(data, ignore_index=False, sort=False,
        keys=bench_callable.index, names=['entity', 'bench'])

    # Concat keep the default index of every data elements. We drop it.
    res = res.droplevel(2)

    return res

def prepend_level(data, key, name):
    return pd.concat([data], keys=[key], names=[name])


class System:
    def __init__(self, context = None, bdd_conn = None):
        self.bench = init_data_frame(['entity', 'bench'], ['callable'])

        self._context = context
        self.bdd_conn = bdd_conn

    def register(self, data):
        '''Register benchs callable with a specific names for different entities.'''
        for entity_name, benchs in data:
            self.register_benchs(entity_name, benchs)

    def register_benchs(self, entity_name, benchs):
        '''Register benchs callable with a specific names for a specific entity.'''
        for bench_name, bench in benchs.items:
            self.register_bench(entity_name, bench_name, bench)

    def register_bench(self, entity_name, bench_name, bench):
        '''Register a bench callable with a specific name for a specific entity.'''
        self.bench.loc[(entity_name, bench_name), :] = [bench]

    def exec(self, entity_names = slice(None), bench_names = slice(None)):
        '''Will run all benchs in the selected range.
        By default, it will run all benchs.'''
        sub_benchs = self.bench.loc[entity_names, bench_names]
        print("Will run the selected area:")
        print(sub_benchs.index)
        res = exec_benchs(sub_benchs)
        res = prepend_level(res, self._context, 'context')
        print(res)
        # self.store(res)

    def store(self, result):
        result.to_sql('benchs', self.bdd_conn, if_exists='append')
        self.bdd_conn.commit()

    def entities(self):
        return np.sort(np.unique(self.bench.index.get_level_values(0)))

    def benchs(self):
        return np.sort(np.unique(self.bench.index.get_level_values(1)))

    def context(self):
        return self._context


# res = dict :
# {
#     'fun1' : {
#         'bench1' : bench_x,
#         'bench2' : bench_y,
#     },
#     'fun2' : {
#         'bench1' : bench_z,
#     }
# }

# Now
# bench = dict :
# {
#     'value1' : 123,
#     'value2' : 456,
# }


# Later :
# bench = dict :
# {
#     'data' : {
#         'value1' : 123,
#         'value2' : 456,
#     },
#     'keep' : {
#         'data' : {
#             'filename' : 'dflasdkf',
#             'ref' : '2344886',
#         },
#         'id' : 'bench_a',
#         'version' : 34,
#     }
# }

# midx :
# midx = pd.MultiIndex.from_product([dims...], dims_names)

# create data :
# mdata = pd.DataFrame(np.random.randn(len(midx)), index=midx)

# send to db :
# mdata.to_sql('data', conn)
# NOTE : lot of adjustment here :
# can insert into view ?
# one attr = 1 table
# create list of attr table
# and create view for each
# can try gather all attr for a sql query

# access db :
# df = pd.read_sql_query('SELECT * FROM data_view',
#       conn, index_col=['commit', 'config', 'entity', 'attr'])

# select sub space of data :
# sub = df.loc['234234', 'x86', 'fun2']
# df.xs(('x86', 'scale','fun1'), level=['config', 'attr', 'entity'])


# store :
