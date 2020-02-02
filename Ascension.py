import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
import time
import random
import glob
import numpy as np
from joblib import Parallel, delayed
import multiprocessing
global File_Location
File_Location=str(os.getcwd())
def retriveemail(line,keyword):
    if f"{keyword}" in line:
        return(True)
def findkeff(line):
    if "keff =" in line:
        keff=line[73:81]
        std=line[122:129]
        return(keff,std)
def spacecut(keff):
    keff=keff.replace(" ",",")
    while ',,' in keff:
        keff.replace(',,',',')
    for i in range(1000):
        keff=keff.replace(f",{i},",f"{i},")
    return(keff)
def runner(name):
    chart=False
    toaddr=""
    keff=""
    try:
        opt=glob.glob('MCNP_AUTO/Music/*.mp3')
        music=opt[random.randint(0,len(opt))]
        mixer.init()
        mixer.music.load(music)
        mixer.music.play()
    except:
        print("Music file not found")
    cpunum=(multiprocessing.cpu_count())
    G=open(name)
    BURNSTATE=np.asarray(list(filter(None,Parallel(n_jobs=-1)(delayed(retriveemail)(line,"BURN") for line in G.readlines()))))
    try:
        BURNSTATE[0]
    except:
        BURNSTATE=np.asarray([False])
    G.close()
    G=open(name)
    Meshstate=np.asarray(list(filter(None,Parallel(n_jobs=-1)(delayed(retriveemail)(meshline,"FMESH") for meshline in G.readlines()))))
    try:
        Meshstate[0]
    except:
        Meshstate=np.asarray([False])
    G.close()
    G=open(name)
    Emesh=np.asarray(list(filter(None,Parallel(n_jobs=-1)(delayed(retriveemail)(meshline,"EMESH") for meshline in G.readlines()))))
    try:
        Emesh[0]
    except:
        Emesh=np.asarray([False])
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
                    keff=f"{keff}{outputname[:outputname.find('.')]},{outputname[outputname.find('.')+1:outputname.find('_')]},{spacecut(line)}"
                if " step  duration     time       power     keff      flux    ave. nu    ave. q    burnup     source" in line:
                    chart=True
                elif "nuclide data are sorted by decreasing" in line or " Individual Material Burnup" in line:
                    chart=False
        else:
            keff=np.asarray(list(filter(None,Parallel(n_jobs=-1)(delayed(findkeff)(line) for line in f.readlines()))))
            if keff.size==0:
                keff=["no keff returned"]
        try:
            mixer.music.fadeout()
        except:
            print("")
        return(BURNSTATE[0],Meshstate[0],Emesh,keff)