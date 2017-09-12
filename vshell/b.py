

arr=[['set_proxy','1.1.1.1','3128','on'],['get_proxy'],['ping','2.2.2.2']]

lst=[]

for i in range(0,len(arr)):
        for j in arr[i]:
            #print(j)
            #print(arr[i])
            #print(('{{{}}}' * len(arr[i])).format(*range(0,len(arr[i]))))
            lst.append(('{{{}}}' * len(arr[i])).format(*range(0,len(arr[i]))))
print(lst)

            #print(''.join(x for x in arr[i]))
