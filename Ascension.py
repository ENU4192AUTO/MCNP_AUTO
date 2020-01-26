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
    if "BURN" in line:
        return(True)
def findkeff(line):
    if "keff =" in line:
        keff=line[73:81]
        std=line[122:129]
        return(keff,std)
def runner(name):
    chart=False
    toaddr=""
    keff=""
    mixer.init()
    mixer.music.load('MCNP_AUTO/duel.mp3')
    mixer.music.play()
    cpunum=(multiprocessing.cpu_count())
    G=open(name)
    BURNSTATE=np.asarray(list(filter(None,Parallel(n_jobs=-1)(delayed(retriveemail)(line) for line in G.readlines()))))
    print(BURNSTATE)
    G.close()
    run_file=name
    short=str(os.path.expanduser('~/mcnp_env_620.bat'))
    input=run_file
    os.system(f"{short}&& mcnp6 i={input} n={input[:len(input)-1]} tasks {cpunum-1}")
    outputname=input[:len(input)-1]+"o"

    with open(outputname,'r') as f:
        if BURNSTATE:
            for line in f.readlines():
                if chart and "         (days)    (days)      (MW)                                           (GWd/MTU)  (nts/sec)" not in line and "nuclide data are sorted by decreasing" not in line and " Individual Material Burnup" not in line:
                    keff=keff+line
                if " step  duration     time       power     keff      flux    ave. nu    ave. q    burnup     source" in line:
                    chart=True
                elif "nuclide data are sorted by decreasing" in line or " Individual Material Burnup" in line:
                    chart=False
        else:
            keff=np.asarray(list(filter(None,Parallel(n_jobs=-1)(delayed(findkeff)(line) for line in f.readlines()))))
            if keff.size==0:
                keff=["no keff returned"]
        mixer.music.stop()
        return(BURNSTATE[0],keff)