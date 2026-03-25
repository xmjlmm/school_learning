# 定义三个列表
a = [1, 2, 3]
b = [4, 5, 6]
c = [4, 5, 6, 7, 8]

 # 打包为元组的列表,而且元素个数与最短的列表一致
a_b = zip(a, b)
# 输出zip函数的返回对象类型
print("a_b类型%s" % type(a_b))
# 输出a_b
print(a_b)

print(list(a_b))

