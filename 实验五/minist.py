import tensorflow as tf
import os
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageFilter
import matplotlib as mpl
import matplotlib.font_manager as fm

# ================== 增强中文字体配置 ==================
def setup_chinese_font():
    """配置中文字体支持，解决中文显示问题"""
    try:
        import platform
        system = platform.system()
        
        if system == 'Windows':
            chinese_fonts = ['Simi', 'Microsoft YaHei', 'SimSun', 'KaiTi', 'FangSong']
        elif system == 'Darwin':
            chinese_fonts = ['PingFang SC', 'STHeiti', 'Apple LiGothic Medium']
        else:
            chinese_fonts = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC']
        
        available_fonts = []
        for font in chinese_fonts:
            try:
                font_path = fm.findfont(fm.FontProperties(family=font))
                if font_path:
                    available_fonts.append(font)
            except:
                continue
        
        if available_fonts:
            plt.rcParams['font.sans-serif'] = available_fonts + ['sans-serif']
            plt.rcParams['axes.unicode_minus'] = False
            print(f"已设置中文字体: {available_fonts[0]}")
        else:
            print("警告: 未找到中文字体，中文可能显示为方框")
            
    except Exception as e:
        print(f"字体设置出错: {e}")
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'KaiTi', 'FangSong']
        plt.rcParams['axes.unicode_minus'] = False

setup_chinese_font()
# ====================================================

# 新增：自定义回调函数用于记录学习率[6,7](@ref)
class LearningRateLogger(tf.keras.callbacks.Callback):
    """自定义回调函数用于记录每个epoch的学习率"""
    def __init__(self):
        super(LearningRateLogger, self).__init__()
        self.lr_history = []
    
    def on_epoch_begin(self, epoch, logs=None):
        # 获取当前学习率
        lr = float(tf.keras.backend.get_value(self.model.optimizer.learning_rate))
        self.lr_history.append(lr)
        print(f"Epoch {epoch+1}: 当前学习率 = {lr:.6f}")

# 1. 加载MNIST数据集
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 2. 增强数据预处理
def enhanced_preprocessing(images):
    """增强的数据预处理流程"""
    # 归一化像素值到[0, 1]范围
    images = images.astype('float32') / 255.0
    
    # 添加通道维度 (height, width) -> (height, width, 1)
    images = np.expand_dims(images, axis=-1)
    
    return images

x_train = enhanced_preprocessing(x_train)
x_test = enhanced_preprocessing(x_test)

# 3. 构建改进的CNN模型（替代简单的全连接网络）
def create_improved_model():
    """创建改进的CNN模型架构"""
    model = tf.keras.models.Sequential([
        # 第一卷积层
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.25),
        
        # 第二卷积层
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.25),
        
        # 全连接层
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.5),
        
        # 输出层
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    return model

model = create_improved_model()

# 4. 编译模型（使用更优化的超参数）
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['sparse_categorical_accuracy']
)

# 5. 设置改进的回调函数
checkpoint_dir = './checkpoint'
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)

checkpoint_save_path = './checkpoint/mnist_cnn_best.weights.h5'

# 早停法防止过拟合
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

# 学习率调度[3,8](@ref)
lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=3,
    min_lr=1e-7,
    verbose=1  # 添加verbose以查看学习率变化
)

# 模型检查点
model_checkpoint = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_save_path,
    save_weights_only=True,
    save_best_only=True,
    monitor='val_sparse_categorical_accuracy',
    mode='max',
    verbose=1
)

# 新增：创建学习率记录器
lr_logger = LearningRateLogger()

# 6. 训练模型（增加训练轮数）
print("开始训练改进的CNN模型...")
history = model.fit(
    x_train, y_train,
    batch_size=128,
    epochs=50,
    validation_data=(x_test, y_test),
    callbacks=[early_stopping, lr_scheduler, model_checkpoint, lr_logger],  # 添加lr_logger
    verbose=1
)

# 7. 显示模型摘要
model.summary()

# 8. 修正的可视化训练过程
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(history.history['sparse_categorical_accuracy'], label='训练准确率')
plt.plot(history.history['val_sparse_categorical_accuracy'], label='验证准确率')
plt.title('训练和验证准确率')
plt.xlabel('训练轮次')
plt.ylabel('准确率')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 3, 2)
plt.plot(history.history['loss'], label='训练损失')
plt.plot(history.history['val_loss'], label='验证损失')
plt.title('训练和验证损失')
plt.xlabel('训练轮次')
plt.ylabel('损失')
plt.legend()
plt.grid(True, alpha=0.3)

# 修正：使用记录的学习率数据而不是history.history['lr']
plt.subplot(1, 3, 3)
plt.plot(lr_logger.lr_history, label='学习率')
plt.title('学习率变化')
plt.xlabel('训练轮次')
plt.ylabel('学习率')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# 9. 在测试集上评估最终模型性能
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f'最终测试准确率: {test_acc:.4f}')
print(f'最终测试损失: {test_loss:.4f}')

# 10. 改进的自定义图像预测
print("\n开始预测自定义图像...")

def preprocess_custom_image(image_path):
    """
    改进的自定义图像预处理函数
    确保与MNIST训练数据预处理一致
    """
    # 加载图像
    img = Image.open(image_path)
    
    # 显示原始图像
    plt.figure(figsize=(6, 6))
    plt.imshow(img, cmap='gray')
    plt.title('原始图像')
    plt.axis('off')
    plt.show()
    
    # 转换为灰度图
    img = img.convert('L')
    
    # 调整大小
    img = img.resize((28, 28), Image.LANCZOS)
    
    # 转换为numpy数组
    img_arr = np.array(img)
    
    # 增强图像对比度（可选）
    img_arr = Image.fromarray(img_arr).filter(ImageFilter.SHARPEN)
    img_arr = np.array(img_arr)
    
    # 应用与MNIST相同的预处理
    # MNIST是黑底白字，自定义图像可能需要反转
    if np.mean(img_arr) > 127:  # 如果图像主要是白色背景
        img_arr = 255 - img_arr  # 反转颜色
    
    # 二值化处理（更智能的阈值）
    threshold = np.mean(img_arr) + np.std(img_arr)  # 动态阈值
    img_arr[img_arr < threshold] = 0
    img_arr[img_arr >= threshold] = 255
    
    # 归一化
    img_arr = img_arr.astype('float32') / 255.0
    
    # 添加通道维度
    img_arr = np.expand_dims(img_arr, axis=-1)
    
    # 显示处理后的图像
    plt.figure(figsize=(6, 6))
    plt.imshow(img_arr[:, :, 0], cmap='gray')
    plt.title('预处理后的图像')
    plt.axis('off')
    plt.show()
    
    return img_arr

# 加载最佳模型
try:
    model.load_weights(checkpoint_save_path)
    print("最佳模型加载成功!")
    
    preNum = int(input("请输入要测试的图片数量: "))
    
    for i in range(preNum):
        image_path = input("请输入测试图片的路径: ")
        
        if not os.path.exists(image_path):
            print(f"错误: 图像文件 {image_path} 不存在!")
            continue
        
        # 使用改进的预处理
        processed_image = preprocess_custom_image(image_path)
        
        # 添加批次维度并进行预测
        x_predict = np.expand_dims(processed_image, axis=0)
        result = model.predict(x_predict, verbose=0)
        predicted_label = np.argmax(result, axis=1)[0]
        confidence = np.max(result)
        
        # 获取前3个最可能的预测结果
        top3_indices = np.argsort(result[0])[-3:][::-1]
        top3_confidences = result[0][top3_indices]
        
        print(f'\n预测结果: {predicted_label}')
        print(f'置信度: {confidence:.4f}')
        print(f'前三预测: {list(zip(top3_indices, top3_confidences))}')
        
        # 显示预测结果
        plt.figure(figsize=(8, 6))
        plt.imshow(processed_image[:, :, 0], cmap='gray')
        plt.title(f'预测: {predicted_label} (置信度: {confidence:.2%})\n前三: {top3_indices[0]}({top3_confidences[0]:.2%}), {top3_indices[1]}({top3_confidences[1]:.2%}), {top3_indices[2]}({top3_confidences[2]:.2%})')
        plt.axis('off')
        plt.show()
        
except Exception as e:
    print(f"发生错误: {e}")
    import traceback
    traceback.print_exc()