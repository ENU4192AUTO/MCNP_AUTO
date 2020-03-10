from os import rename, remove,chdir, system, getcwd
from glob import glob
import numpy as np
try:
    try:
        from TallyScraper import TallyChanger
        from Ascension import runner
    except:
        system("py -m pip install -r requirements.txt")
        from Ascension import runner
        from TallyScraper import TallyChanger
except:
    from Output.MCNP_AUTO import TallyScraper,Ascension
    from Output.MCNP_AUTO.Ascension import runner
    from Output.MCNP_AUTO.TallyScraper import TallyChanger
def auto(couplerun=False):
    G=open("MCNP_AUTO/LOGO.txt")
    logo = G.read()
    G.close()
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
            system(f'title: Attempting Curve Fitting')
        # remove(name[:len(name)-1]+".r")
        # remove(name[:len(name)-1]+".s")
        system(f'title: Automata')
        chdir(cwd)
        print(getcwd())
        rename(name,name+"np")
        if couplerun:
            return(name)

if __name__ == "__main__":
     
    chdir("..")
    auto() 