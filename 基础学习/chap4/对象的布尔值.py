#对象的布尔值
#python一切皆对象，所有对象都有一个布尔值
     #获取对象的布尔值
          #使用内置函数bool（）
#以下对象的布尔值为False
   #False
   #数值（）
   #None
   #空字符串
   #空列表
   #空元组
   #空字典
   #空集合
#测试对象的布尔值
print('-------以下对象的布尔值为False----------------')
print(bool(False)) #False
print(bool(0)) #False
print(bool(0.0)) #False
print(bool(None)) #False
print(bool('')) #False
print(bool("")) #False
print(bool([])) #空列表
print(bool(list())) #空列表
print(bool(())) #空元组
print(bool(tuple())) #空元组
print(bool({})) #空字典
print(bool(dict())) #空字典
print(bool(set())) #空集合

print('-------其它对象的布尔值均为True----------------')
print(bool(18)) #True
print(bool(True))
print(bool('helloworld'))