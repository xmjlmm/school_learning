import tensorflow as tf
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
import numpy as np

# 导入数据，x_train为特征值，y_train为标签
iris = datasets.load_iris()
x_data = iris.data
y_data = iris.target

# 数据标准化 - 非常重要，防止梯度爆炸和NaN损失
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

# 构建网络结构，3个神经元（3分类），softmax激活函数
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(3, activation='softmax')
])

# 在compile中配置训练方法 - 关键修正：使用learning_rate而不是lr
model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.01),  # 同时降低了学习率
              loss='sparse_categorical_crossentropy',
              metrics=['sparse_categorical_accuracy'])

# 打印网络的结构和参数统计
model.build(input_shape=(None, 4))  # 鸢尾花数据集有4个特征
model.summary()

# 训练模型
history = model.fit(x_train, y_train, 
                   epochs=100,
                   validation_split=0.2,
                   verbose=1)

# 评估模型
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f'\nTest accuracy: {test_acc:.2%}')

# 预测示例
test_sample = x_test[0]  # 使用测试集中的样本
x_predict = test_sample[tf.newaxis, ...]  # 添加batch维度
print("x_predict shape:", x_predict.shape)

# 进行预测
result = model.predict(x_predict)
print("Prediction probabilities:", result)

# 获取预测类别
pred = tf.argmax(result, axis=1)
print('\nPredicted class:', pred.numpy())
print("True label:", y_test[0])