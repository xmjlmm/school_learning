import math
a=int(input("请输入a的值为："))
b=int(input("请输入b的值为："))
c=int(input("请输入c的值为："))
s=b*b-4*a*c
if a==0:
    if b==0:
        if c==0:
            print('方程恒成立')
        else:
            print('方程恒不成立')
    else:
        x=-c/b
        print('方程的解为：',x)
else:
    if s<0:
        print('方程无实数解')
    else:
        x1=(-b+math.sqrt(s))/(2*a)
        x2=(-b-math.sqrt(s))/(2*a)
        print('方程的解为{:.2f}\n{:.2f}'.format(x1,x2))