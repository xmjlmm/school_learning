'''
损失函数（loss）：预测值（y）与已知答案（y_）的差距
NN优化目标： loss最小
'''

'''
均方误差mse:
MSE(y_,y) = [((y - y_) ** 2) for i in range(n)] / n
loss_mse = tf.reduce_mean(tf.square(y-y_))
'''

# 损失函数案例

import tensorflow as tf
import numpy as np

SEED = 23455

rdm = np.random.RandomState(seed = SEED)
x = rdm.rand(32,2)
y_ = [[x1 + x2 + (rdm.rand() / 10.0 - 0.05)] for (x1, x2) in x]
x = tf.cast(x, dtype = tf.float32)

w1 = tf.Variable(tf.random.normal([2,1]))

epoch = 15000
lr = 0.002

for epoch in range(epoch):
    with tf.GradientTape() as tape:
        y = tf.matmul(x, w1)
        loss_mse = tf.reduce_mean(tf.square(y_ - y))

    grads = tape.gradient(loss_mse, w1)
    w1.assign_sub(lr * grads)

    if epoch % 500 == 0:
        print('After {} training steps,w1 is {}'.format(epoch, w1))
        print(w1.numpy(),'\n')
print('Final w1 is:', w1.numpy())


# --------------------------------------------------------------------------
print('-----------------------------------------------------------------------------------------------')

'''
自定义损失函数
自定义损失函数 loss(y_, y) = sum[f(y_, y) for i in range(n)]
根据实际情况定义损失函数
'''

# 自定义损失函数案例


import tensorflow as tf
import numpy as np

SEED = 23455
cost = 99
profit = 1

rdm = np.random.RandomState(seed = SEED)
x = rdm.rand(32,2)
y_ = [[x1 + x2 + (rdm.rand() / 10.0 - 0.05)] for (x1, x2) in x]
x = tf.cast(x, dtype = tf.float32)

w1 = tf.Variable(tf.random.normal([2,1]))

epoch = 15000
lr = 0.002

for epoch in range(epoch):
    with tf.GradientTape() as tape:
        y = tf.matmul(x, w1)
        loss_mse = tf.reduce_sum(tf.where(tf.greater(y, y_), (y - y_) * cost, (y_ - y) * profit))

    grads = tape.gradient(loss_mse, w1)
    w1.assign_sub(lr * grads)

    if epoch % 500 == 0:
        print('After {} training steps,w1 is {}'.format(epoch, w1))
        print(w1.numpy(),'\n')
print('Final w1 is:', w1.numpy())


# -----------------------------------------------------------------------------------------------
print('-----------------------------------------------------------------------------------------------')


'''
交叉熵损失函数CE(表征两个概率分布之间的距离)
H（y_, y） = -sum(y_ * lny)
eg:二分类，已知答案y_ = (1, 0), 预测 y1 = (0.6, 0.4) y2 = (0.8, 0.2)
哪个更接近标准答案
H1((1, 0), (0.6, 0.4)) = -(1 * ln(0.6) + 0 * ln(0.4))
H1((1, 0), (0.8, 0.2)) = -(1 * ln(0.8) + 0 * ln(0.2))
因为H1 > H2, 所以y2 预测更准
tf.losses.categorical_crossentropy(y_, y)
'''

# 交叉熵损失函数案例
loss_ce1 = tf.losses.categorical_crossentropy([1,0], [0.6, 0.4])
loss_ce2 = tf.losses.categorical_crossentropy([1,0], [0.8, 0.2])
print('loss_ce1:', loss_ce1)
print('loss_ce2:', loss_ce2)

# -----------------------------------------------------------------------------------------------
print('-----------------------------------------------------------------------------------------------')


# 交叉熵损失函数与softmax结合
# 输出线经过softmax函数，再计算y与y_的交叉熵损失函数
# tf.nn.softmax_cross_entropy_with_logits(y_, y)
y_ = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0]])
y = np.array([[12, 3, 2], [3, 10, 1], [1, 2, 5], [4, 6.5, 1.2], [3, 6, 1]])
y_pro = tf.nn.softmax(y)
loss_ce1 = tf.losses.categorical_crossentropy(y_, y_pro)
loss_ce2 = tf.nn.softmax_cross_entropy_with_logits(y_, y)
print('分布计算的结果：\n', loss_ce1)
print('结合计算的结果：\n', loss_ce2)

