#数据类型
#常用的数据类型
    #整数类型 →int →98
    #浮点数类型→float →3.1159
    #布尔类型 →bool →True.False
    #字符串类型→str→'人生苦短，我用python'


#整数类型
#可以表示正数，负数，0
n1=90
n2=-76
n3=0
print(n1)
print(n2)
print(n3)
print(n1,'类型',type(n1))
print(n2,'类型',type(n2))
print(n3,'类型',type(n3))
#整数可以表示为二进制，十进制，八进制，十六进制
print('十进制',118)
#默认是十进制
print('二进制',0b10101111)   #二进制是以0b开头
print('八进制',0o176)        #八进制是以0o开头
print('十进制',0x1EAF)       #十进制是以0x开头


#浮点类型
   #浮点数整数部分和小数部分组成
   #浮点数存储不精确性
a=3.14159
print(a,type(a))
n1=1.1
n2=2.2
n3=2.1
print(n1+n2)
print(n1+n3)
from decimal import Decimal
print(Decimal('1.1')+Decimal('2.2'))

#布尔类型
    #用来表示真或假的值
    #True表示真，False表示假
    #布尔值可以转化为整数
       #True→1
       #False→0
f1=True
f2=False
print(f1,type(f1))
#布尔值可以转成整数计算
print(f1+1)    #2      1+1的结果为2  True表示1
print(f2+1)    #1      0+1的结果为1  False表示0

#字符串类型
   #字符串又称为不可变的字符序号
   #可以使用单引号''双引号“”三引号''' '''或""" """来定义
   #单引号和双引号定义的字符串必须在一行
   #三引号定义的字符串可以分布在连续的多行
str1='人生苦短，我用python'
print(str1,type(str1))
str2="人生苦短，我用python"
print(str2,type(str2))
str3='''人生苦短，我用python'''
str4="""人生苦短，
我用python"""
print(str3,type(str3))
print(str4,type(str4))

#数据类型转换
#str（）函数与int（）函数
name='张三'
age=20
print(type(name),type(age))   #说明name与age的数据类型不相同
# print('我叫'+name+'今年,'+age+'岁')  #当将str类型与int类型进行连接时，报错，解决方案，类型转换
# +为连接字符
print('我叫'+name+'今年,'+str(age)+'岁')  #将int类型通过str（）函数转成了str类型
print('我叫'+name+',今年'+str(age)+'岁')

#str（）函数 将其他类型转化成字符串
#ps：也可用引号转换
print('-----------str()将其他类型转成str类型---')
a=10
b=198.8
c=False
print(type(a),type(b),type(c))
print(str(a),str(b),str(c),type(str(a)),type(str(b)),type(str(c)))

#int（）函数 将其他类型转化成整数
#ps：1.文字类和小数类字符串，无法转化成整数   2.浮点数转化成整数，抹零取整
print('------------int()将其他类型转int类型---')
s1='128'
f1=98.7
s2='76.77'
ff=True
s3='hello'
print(type(s1),type(f1),type(s2),type(ff),type(s3))
print(int(s1),type(int(s1)))  #将str转成int类型，字符串为数字串
print(int(f1),type(int(f1)))  #将float转成int，截取整数部分，舍掉小数部分
#print(int(s2),type(int(s2))) #将str转成int类型，报错，因为字符串为小数串
print(int(ff),type(int(ff)))
#print(int(s3),type(int(s3)))  #将str转成int类型时，字符串必须为数字串（整数0），非数字串是不允许转换

#float（）函数 将其他数据类型转成浮点数
#ps:1.文字类无法转化成整数                  2.整数转成浮点数，末尾为0
print('------------float()将其他类型转化成float---')
s1='128.98'
s2='76'
ff=True
s3='hello'
i=98
print(type(s1),type(s2),type(ff),type(s3),type(i))
print(float(s1),type(float(s1)))
print(float(s2),type(float(s2)))
print(float(ff),type(float(ff)))
#print(float(s3),type(float(s3)))    #字符串中的数据如果是非数字串，则不允许转换
print(float(i),type(float(i)))