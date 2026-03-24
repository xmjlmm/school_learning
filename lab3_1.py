#a：分子，b：分母，f：符号，t：表示某一项值，s：表示级数和，i：计算器，n:控制循环次数
n=int(input('输入n：'))
a=1
b=1
f=1
t=f*a/b
i=1
s=0
while i<=n:
    s=s+t
    a=1
    b=b+2
    f=-f
    t=f*a/b
    i=i+1
print('当n={}时，pi的近似值是'.format(n),s*4)