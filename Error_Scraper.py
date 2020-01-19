#error scraper 
from glob import glob
import os
import numpy as np
from joblib import Parallel, delayed
os.chdir("..")
try:
    F=open("error.csv",'r')
    F.close()
except:
    F=open("error.csv",'w')
    F.write("Material,Secondary,1-Sigma\n")
    F.close()
def scraper(line):
    if "keff = " in line:
        error=line[122:129]
        return(error)
for name in glob("*.o"):
    G=open(name,'r')
    error=np.asarray(list(filter(None,Parallel(n_jobs=-1)(delayed(scraper)(line) for line in G.readlines()))))
    for item in error:
        F=open("error.csv",'a')
        F.write(f"{name[:name.find('.')]},{name[name.find('.')+1:name.find('_')]},{item}\n")
        F.close()
