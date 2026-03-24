from sklearn import datasets
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# 数据集读入
x_data = datasets.load_iris().data
y_data = datasets.load_iris().target

print('x_data from datasets: \n',x_data)
print('y_data from datasets: \n',y_data)

# 数据集乱序
np.random.seed(116)
np.random.shuffle(x_data)
np.random.seed(116)
np.random.shuffle(y_data)
#tf.random.set_seed(116)

# 数据集分出永不详见的训练集和测试集
x_train = x_data[:-30]
y_train = y_data[:-30]
x_test = x_data[-30:]
y_test = y_data[-30:]

# 转换x的数据类型
x_train = tf.cast(x_train, tf.float32)
x_test = tf.cast(x_test, tf.float32)

# 配成[输入特征，标签]对，每次喂入一小撮(batch)
train_db = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(32)
test_db = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

# 定义神经网络中所有可训练参数
w1 = tf.Variable(tf.random.truncated_normal([4,3], stddev = 0.1, seed = 1))
b1 = tf.Variable(tf.random.truncated_normal([3], stddev = 0.1, seed = 1))

# 定义超参数
lr = 0.1  # 学习率为0.1
train_loss_results = []  # 将每轮的loss记录在此列表中，为后续画loss曲线提供数据
test_acc = []  # 将每轮的acc记录在此列表中，为后续画acc曲线提供数据
epoch = 500   # 循环500轮
loss_all = 0  # 每轮分4个step  loss_all记录四个step生成的4个loss的和

# 嵌套循环迭代，with结构更新参数，显示当前loss
for epoch in range(epoch): #数据集级别迭代
    for step, (x_train, y_train) in enumerate(train_db): # batch级别迭代
        with tf.GradientTape() as tape: # 记录梯度信息
            y = tf.matmul(x_train, w1) + b1  # 神经网络乘加计算
            y = tf.nn.softmax(y)  # 使输出y符合概率分布，此操作后与独热码同量级
            y_ = tf.one_hot(y_train, depth=3)  # 将标签纸转换为独热码格式，方便计算loss值
            loss = tf.reduce_mean(tf.square(y_ - y))  # 采用均方误差损失函数
            loss_all = loss_all + loss.numpy()  # 将每个step计算出的loss数据
            '''
            前向传播计算y
            计算总loss
            '''
        # 计算loss对各个参数的梯度
        grads = tape.gradient(loss, [w1,b1])
        # 实现梯度更新 w1 = w1 - lr * w1_grad   b = b -lr * b1_grad
        # assign_sub赋值操作,更新参数的值并返回
        w1.assign_sub(lr * grads[0])  # 参数w1自更新
        b1.assign_sub(lr * grads[1])  # 参数b1自更新

    # 打印每个epoch, loss信息
    print('Epoch:{}, loss:{}'.format(epoch, loss_all/4))
    train_loss_results.append(loss_all/4)  # 将4个step的loss求平均记录在此变量中
    loss_all = 0  # loss_all归零，为记录下一次epoch的loss做准备

    # 测试部分
    # total_correct为预测对的样本个数， total_number为测试的总样本数， 将两个变量初始化为0
    total_correct, total_number = 0, 0
    for x_test, y_test in test_db:
        # 使用更新后的参数进行预测
        y = tf.matmul(x_test, w1) + b1
        y = tf.nn.softmax(y)
        pred = tf.argmax(y, axis = 1)  # 返回y中最大值的索引，即预测的分类
        # 将pred转换为y_test的数据类型
        pred = tf.cast(pred, dtype = y_test.dtype)
        # 若分类正确，则correct = 1， 否则为0， 将nool型的结果转换为int型
        # tf.equal(A, B)是对比这两个矩阵或者向量的相等的元素, 如果是相等的那就返回True, 否则返回False
        correct = tf.cast(tf.equal(pred, y_test), dtype = tf.int32)
        # 将每个batch的correct数加起来
        correct = tf.reduce_sum(correct)
        # 将所有batch中的correct数加起来
        total_correct = total_correct + int(correct)
        # total_correct为测试的总样本数， 也就是x_test的行数, shape[0]返回变量的行数
        total_number = x_test.shape[0]

    # 总的准确率等于total_correct/total_number
    acc = total_correct / total_number
    test_acc.append(acc)
    print('Test_acc', acc)
    print('---------------------------------------------------------------')

# 绘制 loss 曲线
plt.title('Loss Function Curve')  # 图片标题
plt.xlabel('Epoch')  # y轴变量名称
plt.ylabel('loss')  # x轴变量名称
plt.plot(train_loss_results, label = '$Loss$')  # 逐点画出train_loss_results值并连线
plt.legend()  # 画出曲线图标
plt.show()  # 画出图像

# 画出 Accuracy 曲线
plt.title('Acc Curve')  # 图片标题
plt.xlabel('Epoch')  # y轴变量名称
plt.ylabel('Acc')  # x轴变量名称
plt.plot(test_acc, label = '$Accuracy$')  # 逐点画出train_loss_results值并连线
plt.legend()  # 画出曲线图标
plt.show()  # 画出图像


