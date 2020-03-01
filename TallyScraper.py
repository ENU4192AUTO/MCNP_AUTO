from joblib import Parallel,delayed
import numpy as np
import itertools
import sys
import os
from string import ascii_lowercase
os.system('cls')
def num2str(num):
    alphabets=list(ascii_lowercase)
    return(alphabets[num])
def bufcount(filename):
    f = open(filename)                  
    lines = 0
    buf_size = (1024*25) * (1024*25)
    read_f = f.read # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)
        os.system("cls")
        print(f'Counting file: {filename}\nLines counted: {lines}')

    return lines
def linecheck(line_long):
    line=''
    
    for item in line_long:
        if item==None:
            line=line
        elif "E+00" not in item and "Energy" not in item and "Rel" not in item and "E" in item or "Mesh Tally Number" in item:
            line+=item
    line=line.replace(' ',',')
    while ',,' in line:
        line=line.replace(',,',',')
    line=line.replace('\n,','\n')
    return(line)
def proc(line_long,procnum):
    print(f"starting process {procnum}")
    line=linecheck(line_long)
    if line != linecheck(line_long):
        line=linecheck(line_long)
        print("Error Detected")
    return(line)
def TallyChanger(tallyfile,Emesh=False):
    print(os.getcwd())
    try:
        os.mkdir("Tal_result")
    except:
        pass
    with open(tallyfile) as r: 
        Returns=Parallel(n_jobs=8)(delayed(proc)(i,procnum) for procnum,i in enumerate(itertools.zip_longest(*[r]*(500))))
        Returns=np.asarray(list(filter(None,Returns)))
        if Returns.shape !=(0,):
            for l, sete in enumerate(Returns):
                print(sete.find("Mesh"))
                if "Mesh" in sete:
                    print("In number")
                    try:
                        G.write(sete[1:sete.find("Mesh")])
                        G.close()
                    except:
                        print('')
                    tallynum=sete[sete.find('r')+2:sete.find('r')+4]
                    fnam=f"Tal_result/{tallyfile[:(len(tallyfile)-5)]}_Tally_{tallynum}.csm"
                    G=open(fnam,'w')
                    if Emesh:
                        G.write('Energy,X,Y,Z,Result,Rel_Error \n')
                    else:
                        G.write('X,Y,Z,Result,Rel_Error \n')
                    G.write(sete[sete.find('r')+5:])
                else:
                    G.write(sete[1:])
            G.close()
if __name__ == "__main__":
    os.chdir("..")
    filename=input("Enter the meshtal filename to process:")
    E=input("Enter the Emesh State:")
    TallyChanger(filename)
