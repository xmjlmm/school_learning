'''

f=open("shanghai-metro.txt","r",encoding="utf-8")
data=f.readlines()
f.close()

for i in range(len(data)-1,-1,-1data[i]=data[i].replace("\n","")
    if(data[i]==""):
        data.remove(data[i])

d={}
for i in range(len(data)):
    d[data[i]]=0

for i in range(len(data)):
    d[data[i]]=d[data[i]]+1
print(d)

'''
'''
from pandas import Series
x = Series(['a',True,1], index = ['first','second','third'])
x[1]
#n = Series(['2'])
n = Series(['a',True,1], index = ['first','second','third'])
x = x._append(n)
print(x)
print(x[[0,2,1]])
'''
'''
from pandas import Series
x = Series(['a',True,1], index = ['first','second','third'])
x = x.drop(x,index[3])
print(x)
'''
birth = eval(input('birth = '))
death = eval(input('death = '))
d = {}
for i in range(len(birth)):
    c = birth[i]
    s = death[i]
    while c<=s:
        if c in d:
            d[c] = d[c] + 1
        else:
            d[c] = 0
        c = c + 1
ls = list(d.items())
lst = ls.sort(key = lambda x:x[1] , reverse = True )
print(lst)