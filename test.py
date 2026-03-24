#找到2000到3200年包括在内中所有可以被7整除，但不能被5整除的所有数字，得到的数字按逗号分隔，打印在一行上

#1.输入两数，求两数之和
'''
a=int(input("a="))
b=int(input("b="))
s=a+b
print("s=",s)
'''

#2.数字的阶乘
'''
n=int(input("n="))
i=1
s=1
while i<=n:
    s=i*s
    i+=1
print("s=",s)
'''
#3.计算圆的面积
'''
import math
n=int(input("n="))
s=math.pi*n*n
print("s=",s)
'''
#4.求任意区间内的所有素数
'''
import math
def isPrime(n):
    if(n<2):
        return 0;
    t=int (math.sqrt(n))
    i=2
    while(i<=t):
        if(n%i==0):
            return 0
        i+=1
    return 1
def main():
    count = 0
    n1=int(input("n1="))
    n2=int(input("n2="))
    if(n1<n2):
        n1,n2=n2,n1
    for n in range (n2,n1):
        if isPrime(n)==1:
            print('{:>8}'.format(n),end='')
            count+=1
            if(count%10==0):
                print("\n")
main()

'''
'''
import math
def isPrime(n):
    if n<2:
        return False
    t=int(math.sqrt(n))
    i=2
    while i<=t:
        if n%i==0:
            return False
        i=i+1
    return True
for n in range(2,201):
    if isPrime(n)==True:
        print('{:>8}'.format(n),end='')
'''
#5.求前N个数字的平方和
'''
s=0
N=int(input("N="))
if(N<=0):
    print("输入错误")
else:
    for i in range(1,N+1):
        m=i**2
        s=s+m
print("s=",s)
'''


#6.数字范围内的所有偶数
'''
n1=int(input("n1="))
n2=int(input("n2="))
if(n1<n2):
    n1,n2=n2,n1
for n in range(n2,n1):
    if (n%2==0):
        print(n)
'''

#7.移除列表中的多个元素






