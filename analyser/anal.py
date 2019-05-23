import json
import statistics

dump_map = lambda func, *args : (lambda *args : None)(*map(func, *args))

class Node:
    def __init__(self, op, sub):
        self.__op = op
        self.__sub = sub
        self.__con = []
        self.__ready = False
        self.__value = None

        dump_map(lambda sub : sub.subscribe(self), self.__sub)

    @property
    def ready(self):
        # print("is ready ? {}".format(self.__ready))
        # if self.__ready :
        #     return True

        # self.__ready = all(map(Node.ready, self.__sub))
        # print("all sub ready ? {}".format(self.__ready))
        return self.__ready

    def update(self):
        if self.ready() :
            self.__value = self.__op(*map(Node.get, self.__sub))
            self.notify()
        
    def notify(self):
        print("Notify everybody")
        dump_map(Node.notify, self.__con)

    def subscribe(self, con):
        # print("{} sub to {}".format(str(con), str(self)))
        self.__con.append(con)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        self.__ready = True
        self.notify()


class bench_micro_bench:
    def __init__(self):
        self.reset()

    def reset(self):
        self.raw = None
        self.mean = None
        self.median = None
        self.min = None
        self.max = None
        self.jitter = None
        self.stddev = None

    def set_jitter(self, jitter):
        self.jitter = jitter
    



def parse_stat_file_google_json(file):
    jdata = json.load(file)

    mean = 


def load_stat_file_google_json(filename):
    with open(filename) as f :
        jdata = json.loads(f.read())
    
    return 

def load_stat_file(filename, generator):
    pass

class state:
    def __init__(data):
        self.id = data["commit"]
        self.