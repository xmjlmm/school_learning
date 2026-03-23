fp=open('D:/test.txt','a+')
print(r'hello\tworld',file=fp)
fp.close()


fp=open('D:/test.txt','a+')
print('我说:\'牛逼\'',file=fp)
fp.close()


fp=open('D:/test.txt','a+')
print('我说:\t\'牛逼\'',file=fp)
fp.close()


fp=open('D:/test.txt','a+')
print(r'我说:\b\'酷毙了\'',file=fp)
fp.close()


fp=open('D:/test.doc','a+')
print('hello',file=fp)
fp.close()

fp=open('D:/test.txt','a+')
print('hello\bworld',file=fp)
fp.close()


fp=open('D:/test.txt','a+')
print('helloo\tworld',file=fp)
fp.close()

print(chr(0b100111001011000))
print(ord('乘'))


fp='酷毙了'
print('标识',id(fp))
print('类型',type(fp))
print('值',fp)


fp=('D')



print('“hello”')

n1=3.14
n2=3.1415
n3=n1+n2
print(n3,type(n3))

from decimal import Decimal
print(Decimal('3.14')+Decimal('3.1415'))


num_a=input('请输入第一个整数')
num_b=input('请输入第二个整数')
print(num_a+'大于等于'+num_b    if int(num_a)>=int(num_b)  else  num_a+'小于'+num_b  )

