import pandas
import os
import time
from math import cos,sin,acos,asin,pi
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
def Curve_fit(filename):
    Df=pandas.read_csv(f"Tal_result/{filename[:len(filename)-2]}_Tally_24.csm")
    adjustment=29.11E6/Df.Result.sum()
    adjustment=adjustment/(170/40)
    print(adjustment)
    Df.Result=Df.Result*adjustment
    Df2=pandas.DataFrame(columns=["Z","q'_actual","qcalc","Error"])
    Df2.Z=Df.Z.unique()/100 -(1.7/2)
    for i in range(Df.Z.unique().shape[0]):
        Df2["q'_actual"][i]=(Df[Df.Z==Df.Z.unique()[i]].Result.mean())
    Df2=Df2.sort_values('Z', ascending=True)
    def q_calc(Z,A,B,K,L_e_1,L_e_2,delta,phi_1,phi_2,n,A_exp,w,x_c):
        global qmax
        EXPONENT=A_exp*np.exp(((-w)/x_c)-((-w)/(Z-0.85))-(((Z-0.85)/x_c)**2)*np.exp(-(((-w)/(Z-0.85))-((-w)/x_c))))
        return( qmax*((A*np.cos(pi*Z/L_e_1 + phi_1)+B*np.sin(pi*Z/L_e_2 + phi_2))+ (K/(((Z+ delta))**n )+EXPONENT)))
    global qmax
    qmax=Df2["q'_actual"].max()*1000
    print(qmax)
    Z=Df2.Z.astype(float)
    q=Df2["q'_actual"].astype(float) *1000
    
    params,pc=curve_fit(q_calc,Z,q,maxfev=1000000)
    print(params)
    calc_q=q_calc(Z, params[0], params[1],params[2],params[3],params[4],params[5],params[6],params[7],params[8],params[9],params[10],params[11])
    # plt.plot(Z, calc_q)
    # plt.scatter(Z, q)
    # plt.show()
    # time.sleep(1)
    f=open("Corelation Values.txt",'w')
    f.write(f"{qmax}\n")
    for item in params:
        f.write(f"{item}\n")
    f.close()
    return(qmax, params)
if __name__ == "__main__":

    os.chdir("..")
    Curve_fit("400_layer_2_0.i")