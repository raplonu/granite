from granite.utils.functional import map_at_or_implace
from granite.bench.bench_utils import process_container

def store(bdd_conn, data, context):
    cursor = bdd_conn.cursor()
    for name, benchs in data.items():
        for bench_name, bench in benchs.items():
            data = bench #['data']
            # keep = bench['keep']

            for key, value in data:
                cursor.execute(R"""INSERT INTO data_view VALUES
                ('{commit}', '{config}', '{name}', '{key}', '{value}')""".format(**context, name=name, ))

class System:
    def __init__(self, context, bdd_conn):
        self.data = {}
        self.context = context
        self.bdd_conn = bdd_conn

    def register(self, data):
        self.data.update(data)

    def register_benchs(self, name, benchs):
        elem = map_at_or_implace(self.data, name, {})
        elem.update(benchs)

    def register_bench(self, name, bench_name, bench):
        elem = map_at_or_implace(self.data, name, {})
        elem[bench_name] = bench

    def run(self):
        result = process_container(self.data)
        # Store the result in the bdd

        store(bdd_conn, result)



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
