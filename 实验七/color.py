import tensorflow as tf
import os
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras.layers import Conv2D, MaxPool2D, Flatten, Dense
from tensorflow.keras import Model
from PIL import Image

# 加载CIFAR-10数据集
cifar10 = tf.keras.datasets.cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# 数据预处理：将像素值归一化到0-1范围
x_train, x_test = x_train / 255.0, x_test / 255.0

class LeNet5(Model):
    def __init__(self):
        super(LeNet5, self).__init__()
        self.c1 = Conv2D(filters=6, kernel_size=(5, 5), activation='sigmoid')
        self.p1 = MaxPool2D(pool_size=(2, 2), strides=2)
        
        self.c2 = Conv2D(filters=16, kernel_size=(5, 5), activation='sigmoid')
        self.p2 = MaxPool2D(pool_size=(2, 2), strides=2)
        
        self.flatten = Flatten()
        self.f1 = Dense(units=120, activation='sigmoid')
        self.f2 = Dense(units=84, activation='sigmoid')
        self.f3 = Dense(units=10, activation='softmax')
    
    def call(self, x):
        x = self.c1(x)
        x = self.p1(x)
        x = self.c2(x)
        x = self.p2(x)
        x = self.flatten(x)
        x = self.f1(x)
        x = self.f2(x)
        y = self.f3(x)
        return y

# 创建模型实例
model = LeNet5()

# 编译模型
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['sparse_categorical_accuracy'])

# 设置模型保存路径
checkpoint_save_path = "./checkpoint/LeNet5.weights.h5"  # 使用.weights.h5格式
checkpoint_dir = os.path.dirname(checkpoint_save_path)

# 确保检查点目录存在
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

# 构建模型
model.build(input_shape=(None, 32, 32, 3))

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
    monitor='val_loss'
)

# 训练模型
history = model.fit(x_train, y_train, 
                    batch_size=32, 
                    epochs=10,
                    validation_data=(x_test, y_test),
                    callbacks=[cp_callback])

# 打印网络结构
model.summary()

# 可视化训练过程
acc = history.history['sparse_categorical_accuracy']
val_acc = history.history['val_sparse_categorical_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

# 评估模型
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
print(f'\nTest accuracy: {test_acc:.4f}, Test loss: {test_loss:.4f}')

# 预测部分 - 使用训练好的模型进行预测
model.load_weights(checkpoint_save_path)


img_path = 'F:\\PycharmProjects\\pythonProject\\大四上专项课\\人工智能基础算法（学生版）\\LAB7\\CIFAR10_Lenet5\\car.jpg'
img = Image.open(img_path)
img = img.resize((32, 32), Image.Resampling.LANCZOS)  # 更新了抗锯齿参数
img_arr = np.array(img)

print("Image shape:", img_arr.shape)
plt.imshow(img_arr)
plt.show()

# 预处理图像
img_arr = img_arr / 255.0
# 确保图像有3个通道（如果是灰度图，需要转换为RGB）
if len(img_arr.shape) == 2:
    img_arr = np.stack([img_arr] * 3, axis=-1)
elif img_arr.shape[2] == 1:
    img_arr = np.concatenate([img_arr] * 3, axis=-1)
elif img_arr.shape[2] == 4:
    img_arr = img_arr[:, :, :3]  # 移除alpha通道

x_predict = img_arr[np.newaxis, ...]  # 添加批次维度
print("x_predict shape:", x_predict.shape)

# 进行预测
result = model.predict(x_predict)
print("Prediction probabilities:", result)

pred = tf.argmax(result, axis=1)
print('\nPredicted class:', pred.numpy()[0])