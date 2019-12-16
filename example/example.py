import sys
from granite import GraniteApp
from granite.utils.functional import b_map, boost_fn
from granite.command.decorator import app_command, simple_command
import granite.bench.granite.granite as gr
import sqlite3

conn = sqlite3.connect('me_db.db')
app = GraniteApp('123', conn)

import time
 
def timerfunc(func):
    """
    A timer decorator
    """
    def function_timer(*args, **kwargs):
        """
        A nested function for timing other functions
        """
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        return f"The runtime for {func.__name__} took {runtime} seconds to complete"
    return function_timer

def me_fun(count):
    res = 0
    for e in range(count):
        res += e
    return res

def me_fun2(): 
    return [f"{me_fun(x)}" for x in range(1000)] 



app.register_bench('me_fun',  'granite_micro', gr.f_bench(me_fun, 1000))
app.register_bench('me_fun',  'granite_micro2', gr.f_bench(me_fun, 1000))
app.register_bench('me_fun2', 'granite_micro', gr.f_bench(me_fun2))
app.register_bench('me_fun2', 'granite_micro3', gr.f_bench(me_fun2))


@app_command('user', None, 'This is a app user command, it take the instance')
def user(app, *_):
    print(f'From user : {app}')

@simple_command('very simple', None, 'A very simple command with space !')
def very_simple():
    print('This is a very simple command !!!')

@simple_command('meet', # The command name
    [
        'name', # Positional argument, not restriction
        ('age', {'type':int, 'help' : 'your age using number'})], # Key argument (use -> --age 99)
    'Lets meet !') # Command description
def meet(name, age):
    print(f'Hello {name}, is {age} your age ?')


if __name__ == '__main__':
    sys.exit(app.run(sys.argv[1:]))








# def show_result(obj):
#     print(obj.result)

# app.advertise_system_cmd('result', show_result, 'display raw result structure')


# exe = '../../sandbox/build/benchmark/bench1/SandboxBench1'

# gb1 = format_google_bench <= call_once(google_bench_cmd, exe, 'out.json')

# bin_size = format_binary_size <= call_once(binary_size(exe))

# app.register_bench('bench', lambda : (print('call'), 42)[1])

# app.register_bench('fun_toto', gb1 << 'BM_Fun_toto')
# app.register_bench('fun_tata', gb1 << 'BM_Fun_tata')
# app.register_bench('bin', bin_size)


# register(group_name, bench_name, bench)
# bench return :
# {
#     'data' : { # aka data that is directly send to bdd2
#         'mean' : 13,
#         'stddev' : 345,
#     },
#     'keep' : { # aka data that is need to be keeped and will produce others data
#         'data' : {
#             'filename' : 'ldfj.data',        
#         },
#         'format_id' : id, # stote this data with last id            
#         'format_ver' : last_ver
#     }
# }




