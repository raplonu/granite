## Source of an Alpy

import numpy as mp
import json
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt


from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.key_binding import KeyBindings
from fuzzyfinder import fuzzyfinder

import click

plt.ion()

commit_list = []

data = []


def load_commit_range(nmax = 100):
    '''
    if nmax = None -> load everything
    '''
    if nmax < 0 : nmax = None

    # Open file, read content and parse it as json
    str_data = open("data/commit.json").read()
    data = json.loads(str_data)
    
    # select required data slice
    # If nmax > len(data), the range will stop at len(data)
    return data[:nmax]

# message = click.edit() # Do it in vim

def eval_to_list(args): 
    t = [] 
    for arg in args.split(' '): 
        tmp = None 
        try: 
            tmp = eval(arg) 
        except: 
            tmp = eval('"{}"'.format(arg)) 
        t.append(tmp) 
    return t

def toto(*args):
    print("Toto", args)
    return 'ocucou'


def tata(*args):
    print("Tata", args)
    return 'acucau'



import cmd2 as cmd
from fuzzyfinder import fuzzyfinder

class HelloWorld(cmd.Cmd):
    """Simple command processor example."""
    
    FRIENDS = [ 'Alice', 'Adam', 'Barbara', 'Bob' ]
    
    def do_greet(self, person):
        "Greet the person"
        if person and person in self.FRIENDS:
            greeting = 'hi, %s!' % person
        elif person:
            greeting = "hello, " + person
        else:
            greeting = 'hello'
        print(greeting)
    
    def complete(self, text, state):
        # print("\nText : {}\nState : {}".format(text, state))
        # return cmd.Cmd.complete(self, text, state)
        # print("try with {} and get \n{}".format(self.completenames(''), list(fuzzyfinder(text, self.completenames('')))))
        return list(fuzzyfinder(text, self.completenames('')))
    #     return []
    #     return fuzzyfinder(text, self.complete_help_command('','','',''))

    def complete_greet(self, text, line, begidx, endidx):
        if not text:
            completions = self.FRIENDS[:]
        else:
            completions = fuzzyfinder(text, self.FRIENDS)
        return completions
    
    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    HelloWorld().cmdloop()


# analKeywords = ['help']

class AnalCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, analKeywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


while 1:
    user_input = prompt('> ',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=AnalCompleter())

    try:
        args = parser.parse_args(user_input.split(' '))
        print(args)
        args.cmd()

    except BaseException as be:
        print(be)

    
    
print("Finish")