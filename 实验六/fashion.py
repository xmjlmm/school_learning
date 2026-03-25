import tensorflow as tf
import os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

# -------------------- 1. 数据加载与预处理 --------------------
fashion = tf.keras.datasets.fashion_mnist
(x_train, y_train), (x_test, y_test) = fashion.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# -------------------- 2. 模型构建与编译 --------------------
model = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['sparse_categorical_accuracy'])

# -------------------- 3. 检查点设置与加载 --------------------
checkpoint_dir = "./checkpoint"  # 检查点目录
# 确保检查点目录存在[5](@ref)
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)
    print(f"创建检查点目录: {checkpoint_dir}")

# 修正后的检查点保存路径，以.weights.h5结尾[6](@ref)
checkpoint_save_path = os.path.join(checkpoint_dir, "fashion.weights.h5")

# 检查是否存在之前的检查点并加载[3](@ref)
if os.path.exists(checkpoint_save_path):
    print('-------------加载现有模型------------')
    model.load_weights(checkpoint_save_path)

# 定义ModelCheckpoint回调，正确设置文件路径[6,8](@ref)
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_save_path,  # 使用修正后的路径
    save_weights_only=True,        # 只保存权重
    save_best_only=True,           # 只保存最佳模型
    monitor='val_loss',            # 监控验证损失
    mode='min',                    # 模式为最小化
    verbose=1                      # 显示日志信息
)

# -------------------- 4. 模型训练 --------------------
history = model.fit(x_train, y_train, 
                    batch_size=32, 
                    epochs=5,
                    validation_data=(x_test, y_test),
                    callbacks=[cp_callback])

model.summary()

# -------------------- 5. 可视化训练过程 --------------------
# ... (你的可视化代码保持不变) ...

# -------------------- 6. 预测新图片 --------------------
# 预测时使用与训练时相同的模型结构加载权重[3](@ref)
print("\n-------------开始预测------------")

# 直接使用训练好的模型进行预测，无需重新构建
# 因为我们已经使用了save_best_only=True，训练结束后model已经是最佳状态
# 但更稳妥的做法是从检查点加载最佳权重[7](@ref)
model.load_weights(checkpoint_save_path)

preNum = int(input("请输入要预测的图片数量: "))

for i in range(preNum):
    image_path = input("请输入测试图片的路径: ")
    
    try:
        # 使用PIL处理图片
        img = Image.open(image_path).convert('L')  # 转换为灰度图
        img = img.resize((28, 28))  # 调整大小
        img_arr = np.array(img)
        
        # 预处理：反转和归一化
        img_arr = 255 - img_arr  # 反转颜色（如果背景是黑色）
        img_arr = img_arr / 255.0  # 归一化到[0,1]
        
        # 调整形状以适应模型输入
        x_predict = img_arr[np.newaxis, :, :]  # 增加batch维度
        
        # 预测
        result = model.predict(x_predict)
        pred = np.argmax(result, axis=1)  # 获取预测类别

        print(f'\n图片 {i+1} 的预测结果:')
        print(f"预测类别索引: {pred[0]}")
        print(f"预测类别名称: {class_names[pred[0]]}")
        print(f"各类别概率分布: \n{result}")
        
        # 显示图片
        plt.imshow(img_arr, cmap='gray')
        plt.title(f'Predicted: {class_names[pred[0]]}')
        plt.show(block=False)
        plt.pause(2)
        plt.close()
        
    except Exception as e:
        print(f"处理图片时出错: {e}")