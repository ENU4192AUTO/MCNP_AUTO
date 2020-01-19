try:
    from Ascension import runner
    from glob import glob
    from os import rename, remove
    from os import chdir, system
    import numpy as np
except:
    system("py -m pip install -r requirements.txt")
    from Ascension import runner
    from glob import glob
    from os import rename
    from os import chdir, system
    import numpy as np
chdir("..")
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
    it=0
    for item in keff:
        F=open("keff.csv",'a')
        F.write(f"{name[:name.find('.')]},{name[name.find('.')+1:name.find('_')]},{item[0]},{item[1]}\n")
        F.close()
        it+=1
    system(f'title: Automata')
    rename(name,name+"np")
                               