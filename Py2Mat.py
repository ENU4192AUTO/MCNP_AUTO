import os
def Call(cwd,function:str,Argument1:str,*argv):
    secondaryargs=''
    if isinstance(Argument1, str):
        Argument1=f"\'\"{Argument1}\"\'"
    else:
        Argument1=f"{Argument1}"
    for arg in argv:
        if isinstance(arg, str):
            secondaryargs+=f",\'\"{arg}\"\'"
        else:
            secondaryargs+=f",{arg}"
    allarg=str(Argument1)+str(secondaryargs)
    c=cwd
    print(c)
    input=f"{function}('{c}',{allarg});exit"
    
    os.system(f"matlab -nodisplay -automation -nodesktop -nosplash -wait -r {input} ")
