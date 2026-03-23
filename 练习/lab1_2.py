import math
a=int(input("请输入第一个数"))
b=int(input("请输入第二个数"))
c=int(input("请输入第三个数"))
if a<b+c and b<a+c and c<a+b:
    p=(a+b+c)/2
    s=math.sqrt(p*(p-a)*(p-b)*(p-c))
    print("能构成三角形，三角形的面积为{:.2f}".format(s))
else:
    print("不能构成三角形")
