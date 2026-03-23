# # 创建列表和基本操作
# fruits = ["apple", "banana", "orange", "grape", "kiwi"]
# print("原始列表:", fruits)

# # 访问元素
# print("第一个元素:", fruits[0])           # 正索引
# print("最后一个元素:", fruits[-1])        # 负索引
# print("切片操作:", fruits[1:4])          # 切片 [1](@ref)

# # 添加元素
# fruits.append("mango")                   # 末尾添加
# fruits.insert(2, "pear")                # 指定位置插入
# print("添加元素后:", fruits)

# # 删除元素
# removed = fruits.pop(3)                  # 按索引删除并返回
# fruits.remove("banana")                  # 按值删除
# print(f"删除{removed}后:", fruits)

# # 列表操作
# numbers = [1, 2, 3, 4, 5]
# combined = numbers + [6, 7, 8]          # 列表拼接
# repeated = [0] * 4                      # 列表重复
# print("拼接后:", combined)
# print("重复后:", repeated)

# # 排序和反转
# numbers.sort(reverse=True)               # 降序排序
# fruits.reverse()                        # 反转列表
# print("降序排序:", numbers)
# print("反转列表:", fruits)

# # 其他操作
# print("列表长度:", len(fruits))
# print("orange是否在列表中:", "orange" in fruits)
# print("kiwi出现次数:", fruits.count("kiwi")) 

# # 嵌套列表的创建和访问
# matrix = [
#     [1, 2, 3, 4],
#     [5, 6, 7, 8],
#     [9, 10, 11, 12]
# ]
# print("嵌套矩阵:")
# for row in matrix:
#     print(row)

# # 访问嵌套元素
# print("第二行第三列:", matrix[1][2])     # 输出 7

# # 嵌套列表操作
# student_grades = [
#     ["Alice", [85, 92, 78]],
#     ["Bob", [76, 88, 95]],
#     ["Charlie", [90, 85, 92]]
# ]

# # 计算每个学生的平均分
# for student in student_grades:
#     name = student[0]
#     grades = student[1]
#     avg_grade = sum(grades) / len(grades)
#     print(f"{name}的平均分: {avg_grade:.2f}")

# # 列表推导式处理嵌套列表 [6](@ref)
# # 展平嵌套列表
# nested_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# flattened = [item for sublist in nested_list for item in sublist]
# print("展平后的列表:", flattened)

# # 提取所有学生的成绩
# all_grades = [grade for student in student_grades for grade in student[1]]
# print("所有成绩:", all_grades)


# import copy

# # 1. 直接赋值（引用传递）
# original = [1, 2, [3, 4]]
# assigned = original
# assigned[0] = 100
# print("直接赋值 - 原列表:", original)     # [100, 2, [3, 4]]

# # 2. 浅拷贝
# original = [1, 2, [3, 4]]
# shallow_copy = original.copy()          # 或 original[:]
# shallow_copy[0] = 100                  # 不影响原列表
# shallow_copy[2][0] = 300               # 影响原列表中的嵌套列表
# print("浅拷贝 - 原列表:", original)      # [1, 2, [300, 4]]
# print("浅拷贝 - 新列表:", shallow_copy)   # [100, 2, [300, 4]]

# # 3. 深拷贝
# original = [1, 2, [3, 4]]
# deep_copy = copy.deepcopy(original)
# deep_copy[0] = 100
# deep_copy[2][0] = 300
# print("深拷贝 - 原列表:", original)       # [1, 2, [3, 4]] 不受影响
# print("深拷贝 - 新列表:", deep_copy)      # [100, 2, [300, 4]]

# # 验证对象ID
# print("原始嵌套列表ID:", id(original[2]))
# print("浅拷贝嵌套列表ID:", id(shallow_copy[2]))  
# print("深拷贝嵌套列表ID:", id(deep_copy[2]))     




# # 不同的库导入方式
# import numpy as np
# from numpy import array, arange
# from numpy.random import randn

# # 数组创建的各种方法
# arr1 = np.array([1, 2, 3, 4, 5])                    # 从列表创建
# arr2 = np.arange(0, 10, 2)                         # 类似range函数
# arr3 = np.linspace(0, 1, 5)                        # 等差序列
# arr4 = np.zeros((3, 3))                            # 全零数组
# arr5 = np.ones((2, 4))                             # 全1数组
# arr6 = np.eye(3)                                   # 单位矩阵
# arr7 = np.random.randn(2, 3)                       # 正态分布随机数

# print("一维数组:", arr1)
# print("等差数组:", arr2)
# print("线性空间数组:", arr3)
# print("3x3零矩阵:\n", arr4)
# print("2x4全1矩阵:\n", arr5)
# print("3x3单位矩阵:\n", arr6)
# print("2x3随机矩阵:\n", arr7)


# import numpy as np
# # 数组形状操作
# original = np.arange(12)
# print("原始数组:", original)

# reshaped = original.reshape(3, 4)                  # 改变形状
# flattened = reshaped.flatten()                    # 展平
# transposed = reshaped.T                           # 转置

# print("3x4重塑:\n", reshaped)
# print("转置矩阵:\n", transposed)
# print("展平数组:", flattened)

# # 高级形状操作
# arr_3d = np.arange(24).reshape(2, 3, 4)          # 三维数组
# print("三维数组形状:", arr_3d.shape)
# print("三维数组:\n", arr_3d)

# # 索引和切片
# matrix = np.array([[1, 2, 3, 4],
#                    [5, 6, 7, 8], 
#                    [9, 10, 11, 12]])

# print("原始矩阵:\n", matrix)
# print("第一行:", matrix[0])                       # 行索引
# print("第一列:", matrix[:, 0])                    # 列索引  
# print("子矩阵:\n", matrix[1:3, 1:3])              # 子矩阵
# print("布尔索引:", matrix[matrix > 5])             # 条件索引

# # 花式索引
# fancy_indexed = matrix[[0, 2], [1, 3]]           # (0,1)和(2,3)位置的元素
# print("花式索引结果:", fancy_indexed)


import numpy as np
# 基本数学运算 [12]
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print("数组加法:", a + b)                          # 元素级加法
print("数组乘法:", a * b)                          # 元素级乘法  
print("标量运算:", a * 2)                          # 广播机制
print("矩阵乘法:", np.dot(a.reshape(1, -1), b.reshape(-1, 1)))  # 点积

# 通用函数
print("平方根:", np.sqrt(a))
print("指数:", np.exp(a))
print("对数:", np.log(a))

# 统计方法 [4]
data = np.random.randn(100)                      # 100个随机数

print("基本统计:")
print("平均值:", np.mean(data))
print("中位数:", np.median(data)) 
print("标准差:", np.std(data))
print("方差:", np.var(data))
print("最大值:", np.max(data), "位置:", np.argmax(data))
print("最小值:", np.min(data), "位置:", np.argmin(data))
print("总和:", np.sum(data))
print("累积和:", np.cumsum(data)[-1])

# 多维数组统计
matrix_2d = np.random.randint(0, 100, (4, 5))
print("随机矩阵:\n", matrix_2d)
print("每列平均值:", np.mean(matrix_2d, axis=0))
print("每行最大值:", np.max(matrix_2d, axis=1))
print("整体统计 - 平均值:", matrix_2d.mean(), "标准差:", matrix_2d.std())