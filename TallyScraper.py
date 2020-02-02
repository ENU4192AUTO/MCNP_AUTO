from joblib import Parallel,delayed
import numpy as np
import math
import itertools
import glob
import sys
import pandas as pd
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
        if item is None:
            pass
        elif "E+00" not in item:
            line+=item
    line=line.replace(' ',',')
    while ',,' in line:
        line=line.replace(',,',',')
    line=line.replace('\n,','\n')
    return(line)
def proc(line_long):
    line=linecheck(line_long)
    if line != linecheck(line_long):
        line=linecheck(line_long)
        print("Error Detected")
    return(line)
def TallyChanger(tallyfile,Emesh):
    try:
        os.mkdir("Tal_result")
    except:
        pass
    with open(tallyfile) as r:
        sliceammount=500000
        linecount=bufcount(tallyfile)
        divisor=math.ceil(linecount/sliceammount +1)
        prev=0
        sys.stdout.flush()
        sys.stdout.write(f"Current Line|Max Line \n") 
        counter=0
        for linenum in range(1,divisor):
            starting=prev*sliceammount
            if starting < 14:
                starting =14
            f=itertools.islice(r, starting, linenum*sliceammount)
            prev=linenum
            sys.stdout.write("\r")
            if linenum*sliceammount<linecount:
                currentline=linenum*sliceammount
            else:
                currentline=linecount
            sys.stdout.write(f"{currentline}{' '*(12-len(str(currentline)))}|{linecount}" )
            Returns=Parallel(n_jobs=-1)(delayed(proc)(i) for i in itertools.zip_longest(*[f]*(50000)))
            Returns=np.asarray(list(filter(None,Returns)))
            if Returns.shape !=(0,):
                G=open(f"Tal_result/Mesh_{num2str(counter)}.csv",'w')
                counter+=1
                if Emesh:
                    G.write('Energy,X,Y,Z,Result,Rel_Error, \n')
                else:
                    G.write('X,Y,Z,Result,Rel_Error, \n')
                for l, sete in enumerate(Returns):
                    if l==0:
                       G.write(sete[2:]) 
                    else:
                        G.write(sete[1:])
                G.close()
    os.chdir('Tal_result')
    counter=0
    writer = pd.ExcelWriter(f'Mesh_Tally_{tallyfile}.xlsx', engine='xlsxwriter')
    counter=0
    for csvfile in glob.glob('*.csv'):
        sys.stdout.write("\n")
        sys.stdout.flush()
        sys.stdout.write("\r")
        sys.stdout.write(f"Loading {csvfile} to excel")
        df=pd.read_csv(csvfile)
        df.to_excel(writer, sheet_name=f'Data Part_{counter}')
        counter+=1
        os.remove(csvfile)
    writer.save()