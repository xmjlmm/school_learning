#内置函数range()
#range()函数
     #用于生成一个整数序列
     #创建range对象的三种方式
        #range(stop)--→创建一个（0，stop）之间的整数序列，步长为1
        #range(start,stop)--→创建一个（start，stop）之间的整数序列，步长为1
        #range（start，stop，step）--→创建一个（start，stop）之间的整数序列，步长为step
     #返回值是一个迭代器对象
     #range类型的优点：不管range对象表示的整数序列有多长，所有range对象所用的内存空间都是相同的，
     #因为仅仅需要存储start，stop，step，只有当用到range对象时，才会去计算序数的相关元素
     #in与not in 判断整数序列中是否存在（不存在）指定的整数
#range()的三种创建方式
'''第一种创建方式，只有一个参数（小括号中只给了一个参数）
'''
r=range(10)  #【0，1，2，3，4，5，6，7，8，9】，默认从0开始，默认相差1称为步长
print(r)  #range(0,10)
print(list(r)) #用于查看range对象中的整数序列   --→list是列表的意思

'''第二种创建方式，给了两个参数（小括号中给了两个数）'''
r=range(1,10)  #指定了起始值，从1开始，到10结束（不包含10），默认步长为1
print(list(r)) #[1, 2, 3, 4, 5, 6, 7, 8, 9]

'''第三种创建方式，给了三个参数（小括号中给了三个数）'''
r=range(1,10,2)
print(list(r)) #[1, 3, 5, 7, 9]

'''判断指定的整数，在序列中是否存在 in，not in'''
print(2 in r)
print(10 in r)
print(5 in r)
print(3 in r)
print(10 not in r)

print(range(1,20,1))   #[1...19]
print(range(1,101,1))  #[1...100]