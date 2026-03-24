'''
import math
count=0
for n in range(2,301):
    t=int(math.sqrt(n))
    for i in range(2,t+2):
        if n%i==0:
            break
    if i>t:
        count+=1
        print('{:>8d}'.format(n),end='')
        if count%10==0:
            print()
'''

a = 'hoe'
b = 'fasf'
print(a+b,R'\t',a+b)

li = ['a', 'b', 'mpilgrim', 'z', 'example']
print(li[1: -1])
li.append("new")
li.insert(2,'new')
print(li.index('new'),li.count('new'))
[[1,2],[3,4]]


set1 = {6,7,8,9}
set1.add(5)
print(set1)
set2 = set((5,3,2,2))
print(len(set2))
set3 = set1 | set2
print(len(set3))
print(len(set2 - set1))
list1 = 0


ans = 0
for i in range(1,11):
    res = 1
    for j in range(1,i+1):
        res = res * j
    ans = ans +res
print(ans)