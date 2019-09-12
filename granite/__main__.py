from utils.functional import map_at_or_implace
from bench.bench_utils import process_container

class App:
  def __init__(self):
    self.data = {}

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

def main():
  print(R'''
                            _..._  .--.             __.....__
  .--./)                  .'     '.|__|         .-''         '.
 /.''\\  .-,.--.         .   .-.   .--.    .|  /     .-''"'-.  `.
| |  | | |  .-. |   __   |  '   '  |  |  .' |_/     /________\   \
 \`-' /  | |  | |.:--.'. |  |   |  |  |.'     |                  |
 /("'`   | |  | / |   \ ||  |   |  |  '--.  .-\    .-------------'
 \ '---. | |  '-`" __ | ||  |   |  |  |  |  |  \    '-.____...---.
  /'""'.\| |     .'.''| ||  |   |  |__|  |  |   `.             .'
 ||     || |    / /   | ||  |   |  |     |  '.'   `''-...... -'
 \'. __//|_|    \ \._,\ '|  |   |  |     |   /
  `'---'         `--'  `"'--'   '--'     `'-'
''')
### Credit to http://patorjk.com/software/taag/


if __name__ == "__main__":
    # execute only if run as a script
    main()