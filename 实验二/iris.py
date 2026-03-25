import tensorflow as tf
from sklearn import datasets
from sklearn.preprocessing import StandardScaler  # 用于数据标准化
from matplotlib import pyplot as plt
import numpy as np

# 加载鸢尾花数据集
iris = datasets.load_iris()
x_data = iris.data
y_data = iris.target

# 数据标准化 - 解决数值范围差异大导致的梯度问题 [6,8](@ref)
scaler = StandardScaler()
x_data = scaler.fit_transform(x_data)

# 随机打乱数据
np.random.seed(116)
np.random.shuffle(x_data)
np.random.seed(116)
np.random.shuffle(y_data)
tf.random.set_seed(116)

# 划分训练集和测试集
x_train = x_data[:-30]
y_train = y_data[:-30]
x_test = x_data[-30:]
y_test = y_data[-30:]

# 转换数据类型
x_train = tf.cast(x_train, tf.float32)
x_test = tf.cast(x_test, tf.float32)

# 创建数据集批次
train_db = tf.data.Dataset.from_tensor_slices((x_train, y_train)).batch(32)
test_db = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

# 定义模型参数
w1 = tf.Variable(tf.random.truncated_normal([4, 3], stddev=0.1, seed=1))
b1 = tf.Variable(tf.random.truncated_normal([3], stddev=0.1, seed=1))

# 设置超参数 - 降低学习率防止梯度爆炸 [6,8](@ref)
learnrate = 0.01  # 从0.1降低到0.01
train_loss_results = []
test_acc = []
epochs = 500

# 训练循环
for epoch in range(epochs):
    loss_all = 0
    for step, (x_train_batch, y_train_batch) in enumerate(train_db):
        with tf.GradientTape() as tape:
            # 前向传播
            y = tf.matmul(x_train_batch, w1) + b1
            y_ = tf.one_hot(y_train_batch, depth=3)
            
            # 改用交叉熵损失函数 - 更适合分类问题 [6](@ref)
            loss = tf.reduce_mean(
                tf.keras.losses.categorical_crossentropy(y_, y, from_logits=True))
            
            loss_all += loss.numpy()
            
        # 计算梯度
        grads = tape.gradient(loss, [w1, b1])
        
        # 添加梯度裁剪，防止梯度爆炸 [8](@ref)
        grads = [tf.clip_by_value(g, -1.0, 1.0) for g in grads]
        
        # 更新参数
        w1.assign_sub(learnrate * grads[0])
        b1.assign_sub(learnrate * grads[1])
    
    # 打印训练损失
    avg_loss = loss_all / len(train_db)
    print("Epoch {}, loss: {:.4f}".format(epoch, avg_loss))
    train_loss_results.append(avg_loss)
    
    # 测试准确率
    total_correct, total_number = 0, 0
    for x_test_batch, y_test_batch in test_db:
        # 前向传播
        y = tf.matmul(x_test_batch, w1) + b1
        y = tf.nn.softmax(y)
        pred = tf.argmax(y, axis=1)
        pred = tf.cast(pred, dtype=y_test_batch.dtype)
        
        # 计算正确预测数
        correct = tf.cast(tf.equal(pred, y_test_batch), dtype=tf.int32)
        correct = tf.reduce_sum(correct)
        total_correct += correct
        total_number += x_test_batch.shape[0]
    
    # 计算准确率
    acc = total_correct.numpy() / total_number
    test_acc.append(acc)
    print("Test_acc: {:.2%}".format(acc))
    print("--------------------------")

# 绘制损失曲线和准确率曲线
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.title('Loss Function Curve')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.plot(train_loss_results, label="Loss")
plt.legend()

plt.subplot(1, 2, 2)
plt.title('Accuracy Curve')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.plot(test_acc, label="Accuracy")
plt.legend()

plt.tight_layout()
plt.show()

# 最终评估
final_acc = test_acc[-1]
print("Final test accuracy: {:.2%}".format(final_acc))