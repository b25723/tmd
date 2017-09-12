import random
import itertools
import subprocess

arr=[['set_proxy','1.1.1.1','3128','on'],['get_proxy'],['ping','2.2.2.2']]
inj=['&& id',';id','|id','||id']

def form(cmd):
    lst=[]
    for i in range(0,len(cmd)):
            pos=list(itertools.permutations(range(0,len(cmd[i])),len(cmd[i])))
            #print(pos)
            for j in cmd[i]:
                #lst.append(('{{{}}}' * len(cmd[i])).format(*range(0,len(cmd[i]))))
                for k in range(0,len(pos)):
                    #print(k)
                    injno=k
                    #print(injno)
                    if injno >= len(inj):
                        injno=0
                        lst.append(('{{{}}} ' * (len(cmd[i])+1)).format(*list(itertools.permutations(range(0,len(cmd[i])+1),len(cmd[i])+1))[k]).format(inj[injno],*cmd[i]))
                    else:
                        injno=k
                        #print(injno)
                        lst.append(('{{{}}} ' * (len(cmd[i])+1)).format(*list(itertools.permutations(range(0,len(cmd[i])+1),len(cmd[i])+1))[k]).format(inj[injno],*cmd[i]))

                    #lst.append(('{{{}}} ' * len(cmd[i])).format(*list(itertools.permutations(range(0,len(cmd[i])),len(cmd[i])))[k]).format(*cmd[i]))
    return lst

a=form(arr)
print(a)
print(len(a))
