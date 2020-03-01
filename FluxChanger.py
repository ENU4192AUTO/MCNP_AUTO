import numpy as np
import pandas as pd
import os
from Mesh_analyzer import M_ana
from auto import auto
os.chdir("..")
def Coreadjust(filename,prev,Core):
    rod=0
    check_stat=0
    CORE_FLUX=pd.read_csv(f"Tal_result/{prev}")
    CORE_FLUX=CORE_FLUX[CORE_FLUX.Result != 0]
    MAX_FLUX=(CORE_FLUX.nlargest(100, ['Result'])).sort_values("Result",ascending=False )
    Ave_flux=CORE_FLUX['Result'].mean()
    rod_array,med_array,low_array=M_ana()
    for index,row in MAX_FLUX.iterrows():
        neededchange=(row.Result-Ave_flux)
        x=row.X
        y=row.Y
        X=round((x-round((1.815/2),5))/1.815)
        Y=round((y-round((1.815/2),5))/1.815)
        if X<13 :
            if Y<26:
                Z=6
                X_adj=X
                Y_adj=Y-13
            elif Y<39:
                Z=2
                X_adj=X
                Y_adj=Y-26
        elif X<26:
            if Y<13:
                Z=10
                X_adj=X-13
                Y_adj=Y
            elif Y<26:
                Z=7
                X_adj=X-13
                Y_adj=Y-13
            elif Y<39:
                Z=3
                X_adj=X-13
                Y_adj=Y-26
            else:
                Z=0
                X_adj=X-13
                Y_adj=Y-39
        elif X<39:
            if Y<13:
                Z=11
                X_adj=X-26
                Y_adj=Y
            elif Y<26:
                Z=8
                X_adj=X-26
                Y_adj=Y-13
            elif Y<39:
                Z=4
                X_adj=X-26
                Y_adj=Y-26
            else:
                Z=1
                X_adj=X-26
                Y_adj=Y-39
        else:
            X_adj=X-39
            if Y<26:
                Z=9
                Y_adj=Y-13
            elif Y<39:
                Z=5
                Y_adj=Y-26
        X_adj=int(X_adj)
        Y_adj=int(Y_adj)
        rod_worth=abs(neededchange-rod_array[Z,Y_adj,X_adj])
        med_worth=abs(neededchange-med_array[Z,Y_adj,X_adj])
        low_worth=abs(neededchange-low_array[Z,Y_adj,X_adj])
        if rod_worth<med_worth and rod_worth<low_worth and rod<1:
            Core[Z,Y_adj,X_adj]=16
            rod+=1
        elif med_worth<rod_worth and med_worth<low_worth:
            if Core[Z,Y_adj,X_adj]==35:
                Core[Z,Y_adj,X_adj]=34
            else:
                Core[Z,Y_adj,X_adj]=35
        else:
            if Core[Z,Y_adj,X_adj]==34 and check_stat<5:
                Core[Z,Y_adj,X_adj]=16
                rod+=rod
                check_stat+=1
            else:
                Core[Z,Y_adj,X_adj]=34
        print(f"Assembly:{Z}\n{Core[Z,:,:]}")
    os.chdir("..")
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
    F=open(f"{filename}",'w')    
    F.write(writestr)
    F.close()
    print(f"{rod} rods were used")
    return(Core)
Core=np.zeros((12,13,13),int)
for x,y in [(1,1),(4,1),(8,1),(11,1),(6,2),(3,3),(9,3),(1,4),(6,4),(11,4),(2,6),(4,6),(8,6),(10,6),(1,8),(6,8),(11,8),(3,9),(9,9),(6,10),(1,11),(4,11),(8,11),(11,11)]:
    Core[:,x,y]=2
Core[:,6,6]=3
Core[Core == 0 ]=1
  
for coreset in range(0,20):
    
    if coreset==0:
        prevfilename="Full_Tally_24.csm"
        filename=f"Optimization_{coreset}.i"
    else:
        prevfilename=f"Optimization_{coreset-1}_Tally_24.csm"
        filename=f"Optimization_{coreset}.i"
    Core=Coreadjust(filename,prevfilename,Core)
    auto()
