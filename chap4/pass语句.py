#pass语句
#pass语句
   #语句什么都不做，只是一个占位符，用在语法上需要语句的地方
#什么时候使用：
    #先搭建语法结构，还没想好代码怎么写的时候
#哪些语句一起使用：
   #if语句的条件执行体
   #for-in语句的循环体
   #定义函数时的函数体
#pass语句，什么都不做，只是一个占位符，用到需要写语句的地方
answer=input('您是会员吗？y/n')

#判断是否是会员
if answer=='y':
    pass
else:
    pass


age=int(input('请输入您的年龄：'))

if age:
    print(age)
else:
    print('年龄为:',age)