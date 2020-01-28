from glob import glob
from joblib import parallel, delayed

def spacecut(keff):
    keff=keff.replace("       ",",")
    keff=keff.replace("     ",",")
    keff=keff.replace("    ",",")
    keff=keff.replace("   ",",")
    keff=keff.replace("  ",",")
    for i in range(10000):
        keff=keff.replace(f",{i},",f"{i},")
    return(keff)
G=open("Processed.csv","a")
G.write(f"enrichment,pitch,step,duration,time,power,keff,flux,ave. nu,ave. q,burnup,source\n")
for filename in glob("*.o"):
    keff=""
    BURN=False
    enrichment=filename[:filename.find('.')]
    pitch=filename[filename.find('.')+1:filename.find('_')]
    F=open(filename,'r')
    for line in F.readlines():
        if BURN and "         (days)    (days)      (MW)                                           (GWd/MTU)  (nts/sec)" not in line and "nuclide data are sorted by decreasing" not in line and " Individual Material Burnup" not in line:
                    keff=f"{keff}{enrichment},{pitch},{spacecut(line)}"
        elif " step  duration     time       power     keff      flux    ave. nu    ave. q    burnup     source" in line:
            BURN=True
        elif "nuclide data are sorted by decreasing" in line or " Individual Material Burnup" in line:
            BURN=False 
    F.close()
    G.write(keff)
G.close()
    
