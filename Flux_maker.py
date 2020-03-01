import glob
import numpy as np
import pandas as pd
from os import system, chdir,getcwd
chdir("..")
print(getcwd())
Core=np.zeros((12,13,13),int)
for x,y in [(1,1),(4,1),(8,1),(11,1),(6,2),(3,3),(9,3),(1,4),(6,4),(11,4),(2,6),(4,6),(8,6),(10,6),(1,8),(6,8),(11,8),(3,9),(9,9),(6,10),(1,11),(4,11),(8,11),(11,11)]:
    Core[:,x,y]=2
Core[:,6,6]=3
Core[Core == 0 ]=1
for x in range(0,13,3):
    for y in [1,2,4,5,7,8,10,11]:
        for z in range(0,12):
            for rod in [34,35,16]:
                if Core[z,y,x] != 2 and Core[z,y,x] !=3:
                    Core[z,y,x]=rod
                    newline="]\n"
                    tabline="\n\t\t\t"
                    f0=f" {((np.array2string(Core[0,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    f1=f" {((np.array2string(Core[2,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    f2=f" {((np.array2string(Core[6,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    th6=f" {((np.array2string(Core[11,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    th7=f" {((np.array2string(Core[9,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    th8=f" {((np.array2string(Core[5,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    th9=f" {((np.array2string(Core[1,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    th2=f" {((np.array2string(Core[3,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    th3=f" {((np.array2string(Core[4,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    th0=f" {((np.array2string(Core[7,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    th1=f" {((np.array2string(Core[8,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    O7=f" {((np.array2string(Core[10,:,:]).replace('[','')).replace(newline,tabline)).replace(']]','')}"
                    G=open("Flux_shaping.std",'r')
                    writestr=eval(f'f"""{G.read()}"""')
                    G.close()
                    F=open(f"shaping_data_xe{x}_ye{y}_assemblye{z}_rode{rod}.i",'w')
                    F.write(writestr)
                    F.close()
                    Core[z,y,x]=1