import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

# 设置matplotlib中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示为方块的问题

# -------------------- 1. 数据加载与预处理 --------------------
# 加载Fashion-MNIST数据集[1,2](@ref)
fashion_mnist = tf.keras.datasets.fashion_mnist
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

# 定义类别名称（Fashion-MNIST共有10个类别）[2,5](@ref)
class_names = ['T恤/上衣', '裤子', '套头衫', '连衣裙', '外套',
               '凉鞋', '衬衫', '运动鞋', '包', '短靴']

# 数据预处理[1,2](@ref)
# 将像素值归一化到[0, 1]，并调整形状以适应CNN输入
x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0

# -------------------- 2. 构建改进的CNN模型 --------------------
# 使用更深的CNN架构提高精度[2,3](@ref)
model = models.Sequential([
    # 第一个卷积块
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    
    # 第二个卷积块
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D((2, 2)),
    layers.Dropout(0.25),
    
    # 第三个卷积块
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.25),
    
    # 全连接层
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])

# 打印模型结构
model.summary()

# -------------------- 3. 编译模型 --------------------
# 使用Adam优化器和学习率衰减[3](@ref)
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# -------------------- 4. 设置回调函数 --------------------
# 创建检查点目录
checkpoint_dir = "./checkpoint"
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

# 模型检查点[6](@ref)
checkpoint_path = os.path.join(checkpoint_dir, "best_model.weights.h5")
checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path,
    save_weights_only=True,
    save_best_only=True,
    monitor='val_accuracy',
    mode='max',
    verbose=1
)

# 学习率衰减[3](@ref)
lr_callback = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=2,
    min_lr=0.00001,
    verbose=1
)

# 早停法[3](@ref)
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

# -------------------- 5. 训练模型 --------------------
# 训练模型[1,2](@ref)
history = model.fit(x_train, y_train,
                    batch_size=128,
                    epochs=30,
                    validation_split=0.2,
                    callbacks=[checkpoint_callback, lr_callback, early_stopping])

# -------------------- 6. 评估模型 --------------------
# 加载最佳权重
model.load_weights(checkpoint_path)

# 在测试集上评估模型
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f"\n测试集准确率: {test_acc:.4f}")

# 可视化训练过程
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='训练准确率')
plt.plot(history.history['val_accuracy'], label='验证准确率')
plt.title('模型准确率')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='训练损失')
plt.plot(history.history['val_loss'], label='验证损失')
plt.title('模型损失')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

# -------------------- 7. 预测函数 --------------------
def predict_fashion_image(image_path):
    """
    预测单张服装图像的类别[6](@ref)
    
    Args:
        image_path: 图像文件路径
        
    Returns:
        pred_class: 预测的类别索引
        pred_prob: 预测的置信概率
        class_name: 预测的类别名称
    """
    try:
        # 读取和预处理图像
        img = Image.open(image_path).convert('L')  # 转换为灰度图
        img = img.resize((28, 28))  # 调整大小
        
        # 转换为numpy数组并进行预处理
        img_arr = np.array(img)
        img_arr = 255 - img_arr  # 反转颜色（如果背景是黑色）
        img_arr = img_arr.reshape(1, 28, 28, 1).astype('float32') / 255.0
        
        # 进行预测
        prediction = model.predict(img_arr, verbose=0)
        pred_class = np.argmax(prediction, axis=1)[0]
        pred_prob = np.max(prediction)
        class_name = class_names[pred_class]
        
        return pred_class, pred_prob, class_name
        
    except Exception as e:
        print(f"图像处理错误: {e}")
        return None, None, None

# -------------------- 8. 示例预测 --------------------
# 选择一些测试集样本进行预测
sample_indices = np.random.choice(len(x_test), 9, replace=False)
plt.figure(figsize=(12, 9))

for i, idx in enumerate(sample_indices):
    # 获取样本和真实标签
    sample_img = x_test[idx]
    true_label = y_test[idx]
    true_class = class_names[true_label]
    
    # 预测
    prediction = model.predict(sample_img.reshape(1, 28, 28, 1), verbose=0)
    pred_class = np.argmax(prediction, axis=1)[0]
    pred_prob = np.max(prediction)
    pred_class_name = class_names[pred_class]
    
    # 绘制图像
    plt.subplot(3, 3, i+1)
    plt.imshow(sample_img.reshape(28, 28), cmap='gray')
    
    # 设置标题颜色（绿色正确，红色错误）
    color = 'green' if pred_class == true_label else 'red'
    plt.title(f'真实: {true_class}\n预测: {pred_class_name}\n置信度: {pred_prob:.2%}', 
              color=color, fontsize=9)
    plt.axis('off')

plt.tight_layout()
plt.show()

# -------------------- 9. 保存模型 --------------------
# 保存完整模型
model.save('./fashion_mnist_cnn_model.h5')
print("模型已保存为 'fashion_mnist_cnn_model.h5'")

# -------------------- 10. 使用说明 --------------------
print("\n使用说明:")
print("1. 要预测新图像，请使用 predict_fashion_image('您的图片路径') 函数")
print("2. 图像应为28x28像素的灰度图，或会自动调整大小")
print("3. 模型已保存，下次可直接加载使用: model = tf.keras.models.load_model('fashion_mnist_cnn_model.h5')")

# 示例：加载保存的模型
# loaded_model = tf.keras.models.load_model('./fashion_mnist_cnn_model.h5')