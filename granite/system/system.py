from granite.utils.functional import map_at_or_implace
from granite.bench.bench_utils import process_container

class System:
    def __init__(self):
        self.data = {}
        self.result = {}

    def register(self, data):
        self.data.update(data)

    def register_benchs(self, name, benchs):
        elem = map_at_or_implace(self.data, name, [])
        elem.extend(benchs)

    def register_bench(self, name, bench):
        elem = map_at_or_implace(self.data, name, [])
        elem.append(bench)

    def run(self):
        self.result = process_container(self.data)
        # Store the result in the bdd


