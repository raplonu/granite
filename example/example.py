import sys
import granite.command.app as gap
import granite.command.command as cmd

app = gap.GraniteApp()

def show_result(obj):
    print(obj.result)

app.advertise_system_cmd('result', show_result, 'display raw result structure')


# exe = '../../sandbox/build/benchmark/bench1/SandboxBench1'

# gb1 = format_google_bench <= call_once(google_bench_cmd, exe, 'out.json')

# bin_size = format_binary_size <= call_once(binary_size(exe))

app.register_bench('bench', lambda : (print('call'), 42)[1])

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




if __name__ == '__main__':
    sys.exit(app.run(sys.argv[1:]))
