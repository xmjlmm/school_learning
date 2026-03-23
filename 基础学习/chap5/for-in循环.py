#for-in循环
#for-in循环
   #in表达从（字符串，序列等）中依次取值，又称为遍历
   #for-in遍历的对象必须是可迭代对象
#for-in的语法结构
   #for自定义的变量in可迭代对象：循环体
#for-in的执行图
#循环体内不需要访问自定义变量，可以将自定义变量替代为下划线
for item in 'python':  #第一次取出的p,将p赋值给item，将item的值输出
    print(item)

#range()产生一个整数序列，-->也是一个可迭代对象
for item in range(10):
    print(item)

#如果在循环体中不需要使用到自定义变量,可将自定义变量写为"_"
for _ in range(5):
    print('人生苦短,我用python')

print('使用for循环,计算1到100之间的偶数和')
sum=0  #用于存储偶数和
for item in range(1,101):
    if item%2==0:
        sum+=item
print('1到100之间的偶数和为',sum)