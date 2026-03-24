a=int(input('请输入第一个数为'))
b=int(input('请输入第二个数为'))
c=int(input('请输入第三个数为'))


if a<=b:
    min=a
    min=int(min)
else:
    min=b
    min=int(min)
if min<=c:
    print('最小值为',min)
else:
    print('最小值为',c)
