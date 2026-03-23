#a：分子，b：分母，f：符号，t：表示某一项值，s：表示级数和，i：计算器，n:控制循环次数，x:输出值
x=float(input('输入x的值：'))
n=int(input('输入n的值：'))
a=x**2
b=2.0
f=-1
t=f*a/b
i=1
s=1
while i<=n:
    s=s+t
    i=i+1
    a=a*x*x
    b=b*(2*i-1)*(2*i)
    f=-f
    t=f*a/b
print('Cos(x)的近似值是：',s)