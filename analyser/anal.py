# import json
# import statistics

dump_map = lambda func, *args : (lambda *args : None)(*map(func, *args))

class Node:
    def __init__(self, op = None, *sub):
        self.__op = op
        self.__sub = sub
        self.__con = []
        self.__has_value = False
        self.__value = None

        dump_map(lambda sub : sub.subscribe(self), self.__sub)

    def subscribe(self, con):
        self.__con.append(con)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.__has_value = True
        self.notify()

    def has_value(self):
        return self.__has_value

    def try_update(self):
        if(all(map(Node.has_value, self.__sub))):
            self.value = self.__op(*map(lambda n : n.value, self.__sub))
            self.notify()

    def notify(self):
        dump_map(Node.try_update, self.__con)

    def reset(self):
        self.__value = None
        self.__has_value = False
        dump_map(Node.reset, self.__con)

    def __bool__(self):
        return self.has_value()


class basic_bench:
    def __init__(self):
        self.raw = Node()
        self.mean = Node(statistics.mean, self.raw)
        self.median = Node(statistics.median, self.raw)
        self.min = Node(min, self.raw)
        self.max = Node(max, self.raw)
        self.jitter = Node(lambda a, b : a - b, self.max, self.min)

# class bench_micro_bench:
#     def __init__(self):
#         self.reset()

#     def reset(self):
#         self.raw = None
#         self.mean = None
#         self.median = None
#         self.min = None
#         self.max = None
#         self.jitter = None
#         self.stddev = None

#     def set_jitter(self, jitter):
#         self.jitter = jitter
    



# def parse_stat_file_google_json(file):
#     jdata = json.load(file)

#     mean = 


# def load_stat_file_google_json(filename):
#     with open(filename) as f :
#         jdata = json.loads(f.read())
    
#     return 

# def load_stat_file(filename, generator):
#     pass

# class state:
#     def __init__(data):
#         self.id = data["commit"]
#         self.