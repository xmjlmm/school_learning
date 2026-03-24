import tensorflow as tf
import numpy as np


# 创建int32类型的0维张量，即标量
rank_0_tensor = tf.constant(4)
print(rank_0_tensor)
# 创建float32类型的1维张量
rank_1_tensor = tf.constant([2.0, 3.0, 4.0])
print(rank_1_tensor)
# 创建float16类型的二维张量
rank_2_tensor = tf.constant([[1, 2],
                             [3, 4],
                             [5, 6]], dtype=tf.float16)
print(rank_2_tensor)


# 创建float32类型的张量
rank_3_tensor = tf.constant([
  [[0, 1, 2, 3, 4],
   [5, 6, 7, 8, 9]],
  [[10, 11, 12, 13, 14],
   [15, 16, 17, 18, 19]],
  [[20, 21, 22, 23, 24],
   [25, 26, 27, 28, 29]]])

print(rank_3_tensor)

np.array(rank_2_tensor)


rank_2_tensor.numpy()
# 定义张量a和b
a = tf.constant([[1, 2],
                 [3, 4]])
b = tf.constant([[1, 1],
                 [1, 1]])

print(tf.add(a, b), "\n") # 计算张量的和
print(tf.multiply(a, b), "\n") # 计算张量的元素乘法
print(tf.matmul(a, b), "\n") # 计算乘法
'''
张量也可用于各种聚合运算
tf.reduce_sum()  # 求和
tf.reduce_mean() # 平均值
tf.reduce_max()  # 最大值
tf.reduce_min()  # 最小值
tf.argmax() # 最大值的索引
tf.argmin() # 最小值的索引
'''

c = tf.constant([[4.0, 5.0], [10.0, 1.0]])
# 最大值
print(tf.reduce_max(c))
# 最大值索引
print(tf.argmax(c))
# 计算均值
print(tf.reduce_mean(c))

#变量是一种特殊的张量，形状是不可变，但可以更改其中的参数。定义时的方法是:
my_variable = tf.Variable([[1.0, 2.0], [3.0, 4.0]])
print("Shape: ",my_variable.shape)
print("DType: ",my_variable.dtype)
print("As NumPy: ", my_variable.numpy)



from sklearn import datasets
from pandas import DataFrame
import pandas as pd

x_data = datasets.load_iris().data
y_data = datasets.load_iris().target
print('x_data from datasets: \n',x_data)
print('y_data from datasets: \n',y_data)

x_data = DataFrame(x_data, columns = ['花萼长度', '花萼宽度', '花萼长度', '花萼宽度'])
pd.set_option('display.unicode.east_asian_width', True)
print('x_data add index: \n', x_data)

x_data['类别'] = y_data
print('x_data add a column: \n', x_data)


'''
tf.where()
条件语句真返回A，条件语句假返回B
tf.where(条件语句，真返回A，假返回B)
'''
a = tf.constant([1,2,3,1,1])
b = tf.constant([0,1,3,4,5])
c = tf.where(tf.greater(a,b), a, b)  # 若a>b， 返回a对应位置的元素，否则返回b对应位置的元素
print('c:', c)


import numpy as np
rdm = np.random.RandomState(seed = 1)  # seed = 常数 每次生成随机数相同
a = rdm.rand()  # 返回一个随机标量
b = rdm.rand(2,3)  # 返回维度为2行3列随机数矩阵
print('a', a)
print('b', b)


'''
np.vstack()
将两个数组按垂直方向叠加
np.vstack(数组1,数组2)
'''

import numpy as np
a = np.array([1,2,3])
b = np.array([4,5,6])
c = np.vstack((a, b))
print('c\n', c)

'''

import numpy as np
a = np.array([1,2,3])
b = np.array([4,5,6,7])
c = np.vstack((a, b))
print('c\n', c)
运行不了
'''


'''
np.mgrid[起始值：结束值：步长， 起始值：结束值：步长]
x.ravel() 将x变成以为数组，‘把x变量拉直’
np.c_[] 使返回的间隔数值点配对
'''

import numpy as np
x, y = np.mgrid[1:3:1, 2:4:0.5]
grid = np.c_[x.ravel(), y.ravel()]
print('x:', x)
print('y:', y)
print('grid:\n', grid)









