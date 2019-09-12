import granite



exe = '../../sandbox/build/benchmark/bench1/SandboxBench1'

gb1 = format_google_bench <= call_once(google_bench_cmd, exe, 'out.json')

bin_size = format_binary_size <= call_once(binary_size(exe))

app = granite.App()

res = {}

fun1 = []
fun1.append(gb1 << 'BM_Fun1')
res['fun1'] = fun1

binary = []
binary.append(bin_size)
res['binary'] = binary
