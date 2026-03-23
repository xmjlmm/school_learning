import math
x=float(input('输入x的值：'))
i=1
a=(2*i+1)*x
b=i*(i+1)
s=1
f=1
t=f*a/b
while math.fabs(t)>1e-5:
    s=s+t
    i=i+1
    a=(2*i+1)*(x**i)
    b=i*(i+1)
    f=-f
    t=f*a/b
print('级数的近似值是：',s)