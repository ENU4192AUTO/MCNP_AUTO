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

try:
    F=open("keff.csv",'r')
    F.close()
except:
    F=open("keff.csv",'w')
    F.write("Material,Secondary,K_eff,1-Sigma\n")
    F.close()
for name in glob("*.i"):
    print(name)
    system(f'title Now Running:  {name}')
    toaddr,keff=runner(name)

    for item in keff:
        F=open("keff.csv",'a')
        F.write(f"{name[:name.find('.')]},{name[name.find('.')+1:name.find('_')]},{item[0]},{item[1]}\n")
        F.close()
        it+=1
    # remove(name[:len(name)-1]+".r")
    # remove(name[:len(name)-1]+".s")
    system(f'title: Automata')
    rename(name,name+"np")
                               