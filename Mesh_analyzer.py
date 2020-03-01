import pandas as pd
import numpy as np
from glob import glob
from os import chdir,getcwd
import math
from os import system
import sys
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
def gayround(num):
    bnum=num*1000
    num=str(bnum)
    dec=int(num[num.find('.')+1:num.find('.')+2])
    if dec<6:
        bnum=math.floor(bnum)/1000
    else:
        bnum=math.ceil(bnum)/1000
    return(bnum)
def xyconv(x,y,z,half_pitch=1.815/2):
    x=(x*1.815) + half_pitch
    y=(y*1.815) + half_pitch
    if z==0 or z==3 or z==7 or z==10:
        x=x+(23.595*1)
    elif z==1 or z==4 or z==8 or z==11:
        x=x+(23.595*2)
    elif z==5 or z==9:
        x=x+(23.595*3)
    if z==2 or z==3 or z==4 or z==5:
        y=y+(23.595*1)
    elif z==6 or z==7 or z==8 or z==9:
        y=y+(23.595*2)
    elif z==10 or z==11:
        y=y+(23.595*3)
    x=gayround(round(x,4))
    y=gayround(round(y,4))
    if x== 22.687:
        x=22.688
    if y==22.687:
        y=22.688 
    return(x,y)
def coremap(x_core,y_core,Ana):
    Ana.X=Ana.X.round(4)
    X_val=pd.DataFrame(Ana.loc[(Ana.X==x_core)])
    if X_val.shape[0]==0:
        X_val=pd.DataFrame(Ana.loc[(Ana.X==x_core+.001)])
    X_val.Y=X_val.Y.round(4)
    val=X_val.loc[X_val.Y==y_core,'Result']
    if val.shape[0]==0:
        val=X_val.loc[X_val.Y==y_core+.001,'Result']
    if val.shape[0]==0:
        return(999)
    newval=float(val)
    return(newval)
def M_ana():
    chdir("Tal_result")
    # half_pitch=1.815/2
    print(getcwd())
    Base_flux=pd.read_csv("Full_Tally_24.csm")
    Base_flux = Base_flux[Base_flux.Result != 0]
    # Base_fissions=pd.read_csv("Full_Tally_24.csm")
    # rod_arrayf=np.zeros((12,13,13),float)
    # med_arrayf=np.zeros((12,13,13),float)
    # low_arrayf=np.zeros((12,13,13),float)
    rod_array=np.zeros((12,13,13),float)
    med_array=np.zeros((12,13,13),float)
    low_array=np.zeros((12,13,13),float)
    for  file in (glob("*.csv")):
        x=int(file[file.find('xe')+2:file.find("_y")])
        y=int(file[file.find('ye')+2:file.find("_assembly")])
        z=int(file[file.find('assemblye')+9:file.find("_rod")])
        rod=int(file[file.find('rode')+4:file.find("_Tally")])
        Ana=pd.read_csv(file)
        Ana = Ana[Ana.Result != 0]
        y_core,x_core=xyconv(x,y,z)
        # if x_core == 24.502 and y_core== 82.582:
            # print("this")
        if "24" in file:
            val=coremap(x_core,y_core,Ana)
            base_val=coremap(x_core,y_core,Base_flux)
            if rod==16:
                rod_array[z,y,x]=base_val-((val))
            elif rod==35:
                med_array[z,y,x]=base_val-((val))
            elif rod==34:
                low_array[z,y,x]=base_val-((val))
    for array in [rod_array,med_array,low_array]:
        for x in range(13):
            
            for z in range(12):
                
                for y in [0,3,6,9,12]:    
                    # sys.stdout.write(f"Processing {z},{x},{y}\n")
                    if array[z,x,y] <0:
                        array[z,x,y]=abs(array[z,x,y])
                for y in [1,4,7,10]:
                    # sys.stdout.write(f"Processing {z},{x},{y}\n")
                    # sys.stdout.write(f"{array[z,x,y]},")
                    l=array[z,x,y-1]
                    r=array[z,x,y+2]
                    
                    dy=(r-l)/3
                    
                    array[z,x,y]=l+dy
                    # sys.stdout.write(f"{dy},{array[z,x,y]}\n")
                for y in [2,5,8,11]:
                    # sys.stdout.write(f"Processing {z},{x},{y}\n")
                    # sys.stdout.write(f"{array[z,x,y]},")
                    l=array[z,x,y-2]
                    r=array[z,x,y+1]
                    
                    dy=(r-l)*(2/3)
                    
                    array[z,x,y]=l+dy
                    # sys.stdout.write(f"{dy},{array[z,x,y]}\n")
    return(rod_array,med_array,low_array)