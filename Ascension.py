import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
import time
import numpy as np
from joblib import Parallel, delayed
import multiprocessing
global File_Location
File_Location=str(os.getcwd())
def retriveemail(line):
    if "Email:" in line:
        emailadd=line[line.find(":")+1:len(line)-1]
        return(emailadd)
def findkeff(line):
    if "keff =" in line:
        keff=line[73:81]
        std=line[122:129]
        return(keff,std)
def runner(name):
    cpunum=(multiprocessing.cpu_count())
    G=open(name)
    toaddr=np.asarray(list(filter(None,Parallel(n_jobs=-1)(delayed(retriveemail)(line) for line in G.readlines()))))
    G.close()
    run_file=name
    short=str(os.path.expanduser('~/mcnp_env_620.bat'))
    input=run_file
    os.system(f"{short}&& mcnp6 i={input} n={input[:len(input)-1]} tasks {cpunum-1}")
    outputname=input[:len(input)-1]+"o"
    with open(outputname,'r') as f:
        keff=np.asarray(list(filter(None,Parallel(n_jobs=-1)(delayed(findkeff)(line) for line in f.readlines()))))
        if keff.size==0:
            keff=["no keff returned"]
        return(toaddr,keff)