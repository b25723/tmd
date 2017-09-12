import random
import itertools

arr=[['set_proxy','1.1.1.1','3128','on'],['get_proxy'],['ping','2.2.2.2']]

def form(cmd):
    lst=[]
    for i in range(0,len(cmd)):
            for j in cmd[i]:

                #lst.append(('{{{}}}' * len(cmd[i])).format(*random.sample(range(0,len(cmd[i])),len(cmd[i]))))
                lst.append(('{{{}}}' * len(cmd[i])).format(*itertools.permutations(range(0,len(cmd[i])),len(cmd[i]))))
    return lst

a=form(arr)
print(a)
print(len(a))
