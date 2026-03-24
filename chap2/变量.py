name='马丽亚'
print(name)

#变量由三部分组成
#标识：表示对象所存储的内存地址，使用内置函数id（obj）来获得
#类型：表示的是对象的数据类型，使用内置函数type（obj）来获取
#值：表示对象所存储的具体数据，使用print（obj）可以将值进行打印输出

name='马丽亚'
print(name)
print('标识',id(name))
print('类型',type(name))
print('值',name)

#当多次赋值之后，变量名会指向新的空间
name='马丽亚'
print(name)
name='楚留冰'
print(name)

name='马丽亚'
name='楚留冰'
print(name)