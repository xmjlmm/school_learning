import math
a = float(input('请输入a的值为：'))
b = float(input('请输入b的值为：'))
c = float(input('请输入c的值为：'))
if a == 0:
    if b == 0:
        if c == 0:
            print('方程恒成立')
        else:
            print('方程恒不成立')
    else:
        x = -c / b
        print('方程只有唯一解，解为：{}'.format(x))
else:
    delta = b * b - 4 * a * c
    if delta >= 0:
        x1 = (-b + math.sqrt(delta)) / (2 * a)
        x2 = (-b - math.sqrt(delta)) / (2 * a)
        print('方程有两个实根，解分别为：x1={:.2f} \n\t\t\t  x2={:.2f}'.format(x1, x2))
    else:
        m = -b / (2 * a)
        n = math.sqrt(-delta) / (2 * a)
        print('方程有两个虚根，分别为：x1={}+{}i \n\t\t\tx2={}-{}i'.format(m, n, m, n))
