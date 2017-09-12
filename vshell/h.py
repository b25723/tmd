import random
import itertools
import subprocess
import logging
import unittest


#arr=[['set_proxy','1.1.1.1','3128','on'],['get_proxy'],['ping','2.2.2.2']]
#arr=[['get_proxy'],['ping','2.2.2.2']]
arr=[['ifconfig','eth0'],['ls','/tmp/']]
inj=['&&id',';id','|id','||id']
#inj=itertools.cycle(['&& id',';id','|id','||id'])

def form(cmd):
    lst=[]
    for i in range(0,len(cmd)):
            pos=list(itertools.permutations(range(0,len(cmd[i])),len(cmd[i])))
            #for j in cmd[i]:
            for j in range(0,len(cmd[i])):
                for k in range(0,len(pos)):
                    for l in range(0,len(inj)):
                        #lst.append(('{{{}}} ' * (len(cmd[i])+1)).format(*list(itertools.permutations(range(0,len(cmd[i])+1),len(cmd[i])+1))[k]))
                        lst.append(('{{{}}} ' * (len(cmd[i])+1)).format(*list(itertools.permutations(range(0,len(cmd[i])+1),len(cmd[i])+1))[k]).format(*cmd[i]+[''.join(inj[l])]))

    return lst

#a=form(arr)
#print(a)
#print(len(a))
a=form(arr)
for i in a:
    print(i)
    #print(subprocess.check_output(a,shell=True))
