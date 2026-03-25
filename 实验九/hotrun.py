import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, SimpleRNN, Embedding
import matplotlib.pyplot as plt
import os

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 字母映射到数值id的词典
w_to_id = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
           'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19,
           'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25}

# 创建训练集：每4个字母预测下一个字母
x_train = []
y_train = []

# 在26个字母中设置每4个推导后面一个数据
for i in range(4, 26):
    # 获取当前字母和前3个字母的ID
    current_sequence = [w_to_id[chr(97 + j)] for j in range(i-4, i)]  # 97是'a'的ASCII码
    x_train.append(current_sequence)
    # 下一个字母作为目标
    y_train.append(w_to_id[chr(97 + i)])

# 随机打乱数据，使用相同的种子，保证输入特征和标签一一对应
np.random.seed(7)
np.random.shuffle(x_train)
np.random.seed(7)
np.random.shuffle(y_train)
tf.random.set_seed(7)

# 使x_train符合Embedding输入要求：[送入样本数，循环核时间展开步数]
x_train = np.reshape(x_train, (len(x_train), 4))
y_train = np.array(y_train)

# 搭建RNN循环神经网络
model = tf.keras.Sequential([
    Embedding(26, 2),  # 26表示词汇表长度，2表示编码维度
    SimpleRNN(10),     # RNN层，10个记忆体
    Dense(26, activation='softmax')  # 全连接层，26个神经元对应26个字母的概率
])

# 配置模型训练方法
model.compile(optimizer=tf.keras.optimizers.Adam(0.01),
              loss='sparse_categorical_crossentropy',
              metrics=['sparse_categorical_accuracy'])

# 设置模型保存路径
checkpoint_save_path = "./checkpoint/rnn_embedding_4pre1.weights.h5"  # 使用.weights.h5格式

# 确保检查点目录存在
if not os.path.exists(os.path.dirname(checkpoint_save_path)):
    os.makedirs(os.path.dirname(checkpoint_save_path))

# 构建模型
model.build(input_shape=(None, 4))

# 检查是否存在权重文件并尝试加载
if os.path.exists(checkpoint_save_path):
    try:
        print('-------------加载已有模型-----------------')
        model.load_weights(checkpoint_save_path)
        print('-------------权重加载成功-----------------')
    except (ValueError, OSError) as e:
        print(f'-------------权重加载失败: {e}-----------------')
        print('-------------将重新训练模型-----------------')
else:
    print('-------------从头开始训练模型-----------------')

# 设置模型检查点回调
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_save_path,
    save_weights_only=True,
    save_best_only=True,
    monitor='loss'  # 监控训练损失
)

# 训练模型
history = model.fit(x_train, y_train, 
                    batch_size=32, 
                    epochs=100, 
                    callbacks=[cp_callback],
                    verbose=1)

# 打印网络结构
model.summary()

# 可视化训练过程
acc = history.history['sparse_categorical_accuracy']
loss = history.history['loss']

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(acc, label='训练准确率')
plt.title('训练准确率')
plt.xlabel('Epoch')
plt.ylabel('准确率')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(loss, label='训练损失')
plt.title('训练损失')
plt.xlabel('Epoch')
plt.ylabel('损失')
plt.legend()

plt.tight_layout()
plt.show()

# 预测部分
input_word = "abcdefghijklmnopqrstuvwxyz"

# 加载模型权重进行预测
model.build(input_shape=(None, 4))
model.load_weights(checkpoint_save_path)

# 进行预测
preNum = int(input("input the number of test alphabet: "))

for i in range(preNum):
    alphabet1 = input("input test alphabet: ")
    
    # 确保输入是4个字母
    if len(alphabet1) != 4:
        print("请输入恰好4个字母!")
        continue
    
    # 将字母转换为ID
    alphabet = [w_to_id[a] for a in alphabet1]
    
    # 重塑为适合模型的形状
    alphabet = np.reshape(alphabet, (1, 4))
    
    # 进行预测
    result = model.predict(alphabet, verbose=0)
    pred = tf.argmax(result, axis=1)
    pred = int(pred.numpy())
    
    # 输出预测结果
    print(f"{alphabet1} -> {input_word[pred]}")