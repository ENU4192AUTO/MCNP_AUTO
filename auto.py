from os import rename, remove,chdir, system

try:
    from Ascension import runner
    from glob import glob
    from os import rename, remove,chdir, system

    import numpy as np
except:
    system("py -m pip install -r requirements.txt")
    from Ascension import runner
    from glob import glob
    from os import  rename, remove,chdir, system
    import numpy as np
G=open("LOGO.txt")
logo = G.read()
G.close()
chdir("..")
logo=eval(f'f"""{logo}"""')
print(f"{logo}\nThe program will run {len(glob('*.i'))} .i files")


for name in glob("*.i"):
    print(name)
    system(f'title Now Running:  {name}')
    Burnstate,keff=runner(name)
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
    # remove(name[:len(name)-1]+".r")
    # remove(name[:len(name)-1]+".s")
    system(f'title: Automata')
    rename(name,name+"np")
                               