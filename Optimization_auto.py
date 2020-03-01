from os import rename, remove,chdir, system, getcwd
import sys
try:
    from TallyScraper import TallyChanger
    from Ascension import runner
    from Mesh_analyzer import M_ana
    from glob import glob
    import numpy as np
    import pandas as pd
except:
    system("py -m pip install -r requirements.txt")
    from Ascension import runner
    from Mesh_analyzer import M_ana
    from glob import glob
    from os import  rename, remove,chdir, system
    import numpy as np
    from TallyScraper import TallyChanger
    import pandas as pd
G=open("LOGO.txt")
logo = G.read()
G.close()
chdir("..")
cwd=getcwd()
logo=eval(f'f"""{logo}"""')
print(f"{logo}\nThe program will run {len(glob('*.i'))} .i files")


for name in glob("*.i"):
    print(name)
    Burnstate,Meshstate,Emesh,keff=runner(name)
    print(Burnstate)
    if Burnstate:
        try:
            F=open("results.csv",'r')
            F.close()
        except:
            F=open("results.csv",'w')
            F.write("FirstVar,SecondVar,step,duration,time,power,keff,flux,ave. nu,ave. q,burnup,source\n")
            F.close()
        F=open("results.csv",'a')
        F.write(f"{keff}")
        F.close()
    else:
        for item in keff:
            try:
                    F=open("keff.csv",'r')
                    F.close()
            except:   
                F=open("keff.csv",'w')
                F.write("Material,Secondary,K_eff,1-Sigma\n")
                F.close()
            F=open("keff.csv",'a')
            F.write(f"{name[:name.find('.')]},{name[name.find('.')+1:name.find('_')]},{item[0]},{item[1]}\n")
            F.close()
    if Meshstate:
        TallyChanger(name[:len(name)-1]+"msht",Emesh)
    remove(name[:len(name)-1]+"r")
    remove(name[:len(name)-1]+"s")
    remove(name[:len(name)-1]+"msht")
    system(f'title: Automata')
    chdir(cwd)
    print(getcwd())
    rename(name,name+"np")
rod_array,med_array,low_array=M_ana()

F=open("rod_array.arr",'w')
for item in range(12):
    rod_array_saver=np.array2string(rod_array[item,:,:])
    F.write(rod_array_saver)
F.close()
F=open("med_array.arr",'w')
for item in range(12):
    med_array_saver=np.array2string(med_array[item,:,:])
    F.write(med_array_saver)
F.close()
F=open("low_array.arr",'w')
for item in range(12):
    low_array_saver=np.array2string(low_array[item,:,:])
    F.write(low_array_saver)
    
F.close()
