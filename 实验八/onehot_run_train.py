import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, SimpleRNN, Embedding
import matplotlib.pyplot as plt
import os
import shutil

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 字母到数值id的映射
w_to_id = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4}
id_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e'}

# 设置训练集
x_train = [w_to_id['a'], w_to_id['b'], w_to_id['c'], w_to_id['d'], w_to_id['e']]
y_train = [w_to_id['b'], w_to_id['c'], w_to_id['d'], w_to_id['e'], w_to_id['a']]

# 随机打乱数据
np.random.seed(7)
np.random.shuffle(x_train)
np.random.seed(7)
np.random.shuffle(y_train)
tf.random.set_seed(7)

# 重塑数据以适应RNN输入
x_train = np.reshape(x_train, (len(x_train), 1))
y_train = np.array(y_train)

# 搭建RNN循环神经网络 - 使用3个记忆体
model = tf.keras.Sequential([
    Embedding(5, 2),  # 输入词汇表大小为5，输出维度为2
    SimpleRNN(3),    # RNN层，3个记忆体
    Dense(5, activation='softmax')  # 全连接层，5个神经元
])

# 配置模型训练方法
model.compile(optimizer=tf.keras.optimizers.Adam(0.01),
              loss='sparse_categorical_crossentropy',
              metrics=['sparse_categorical_accuracy'])

# 设置模型保存路径
checkpoint_save_path = "./checkpoint/run_embedding_1pre1.weights.h5"
checkpoint_dir = os.path.dirname(checkpoint_save_path)

# 确保检查点目录存在
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

# 检查权重兼容性的函数
def check_weight_compatibility(model, checkpoint_path):
    """检查模型与保存的权重是否兼容"""
    if not os.path.exists(checkpoint_path):
        return False
        
    try:
        # 临时构建模型
        model.build(input_shape=(None, 1))
        # 尝试加载权重但不应用（用于检查兼容性）
        model.load_weights(checkpoint_path, skip_mismatch=False)
        return True
    except (ValueError, OSError, IndexError) as e:
        print(f"权重不兼容: {e}")
        return False

# 构建模型
model.build(input_shape=(None, 1))

# 检查权重兼容性并处理
if os.path.exists(checkpoint_save_path):
    if check_weight_compatibility(model, checkpoint_save_path):
        print('-------------加载已有模型-----------------')
        model.load_weights(checkpoint_save_path)
    else:
        print('-------------权重不兼容，删除旧权重并重新训练-----------------')
        # 删除旧的权重文件
        if os.path.exists(checkpoint_dir):
            shutil.rmtree(checkpoint_dir)
            os.makedirs(checkpoint_dir)
else:
    print('-------------从头开始训练模型-----------------')

# 设置模型检查点回调
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_save_path,
    save_weights_only=True,
    save_best_only=True,
    monitor='loss',
    mode='min'
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
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history['sparse_categorical_accuracy'], label='训练准确率')
plt.title('训练准确率')
plt.xlabel('Epoch')
plt.ylabel('准确率')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='训练损失')
plt.title('训练损失')
plt.xlabel('Epoch')
plt.ylabel('损失')
plt.legend()

plt.tight_layout()
plt.show()

# 评估模型
print("模型评估:")
train_loss, train_acc = model.evaluate(x_train, y_train, verbose=0)
print(f"训练损失: {train_loss:.4f}, 训练准确率: {train_acc:.4f}")

# 预测函数
def predict_next_letter(model, current_letter):
    """预测给定字母的下一个字母"""
    if current_letter not in w_to_id:
        raise ValueError(f"字母 '{current_letter}' 不在词汇表中")
    
    current_id = w_to_id[current_letter]
    input_data = np.reshape([current_id], (1, 1))
    
    prediction = model.predict(input_data, verbose=0)
    predicted_id = np.argmax(prediction)
    confidence = np.max(prediction)
    
    predicted_letter = id_to_letter[predicted_id]
    
    return predicted_letter, confidence

# 测试所有字母的预测
print("\n预测结果:")
for letter in ['a', 'b', 'c', 'd', 'e']:
    predicted_letter, confidence = predict_next_letter(model, letter)
    print(f"{letter} -> {predicted_letter} (置信度: {confidence:.3f})")