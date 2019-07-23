## Source of an Alpy

import numpy as mp
import json
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
plt.ion()

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

    
print("Hello, welcome to ...")
print('''
   ____    ,---.   .--.   ____      .---.       ____     __  .-'\''-.     .-''-.  .-------.     
 .'  __ `. |    \  |  | .'  __ `.   | ,_|       \   \   /  // _     \  .'_ _   \ |  _ _   \    
/   '  \  \|  ,  \ |  |/   '  \  \,-./  )        \  _. /  '(`' )/`--' / ( ` )   '| ( ' )  |    
|___|  /  ||  |\_ \|  ||___|  /  |\  '_ '`)       _( )_ .'(_ o _).   . (_ o _)  ||(_ o _) /    
   _.-`   ||  _( )_\  |   _.-`   | > (_)  )   ___(_ o _)'  (_,_). '. |  (_,_)___|| (_,_).' __  
.'   _    || (_ o _)  |.'   _    |(  .  .-'  |   |(_,_)'  .---.  \  :'  \   .---.|  |\ \  |  | 
|  _( )_  ||  (_,_)\  ||  _( )_  | `-'`-'|___|   `-'  /   \    `-'  | \  `-'    /|  | \ `'   / 
\ (_ o _) /|  |    |  |\ (_ o _) /  |        \\      /     \       /   \       / |  |  \    /  
 '.(_,_).' '--'    '--' '.(_,_).'   `--------` `-..-'       `-...-'     `'-..-'  ''-'   `'-'   
                                                                                               
''')





commit_list = []

data = []

def update_data(nmax = 100):
    global data
    data = load_commit_range(nmax)

