import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False      # 解决负号显示问题

# 1. 加载和预处理数据
def load_and_preprocess_data():
    """加载MNIST数据集并进行预处理"""
    print("正在加载MNIST数据集...")
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
    
    # 数据预处理
    # 将图像数据从[0, 255]归一化到[0, 1]范围，并添加通道维度
    train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
    test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255
    
    print(f"训练集形状: {train_images.shape}, 标签形状: {train_labels.shape}")
    print(f"测试集形状: {test_images.shape}, 标签形状: {test_labels.shape}")
    
    return (train_images, train_labels), (test_images, test_labels)

# 2. 构建CNN模型
def create_cnn_model():
    """创建卷积神经网络模型"""
    print("构建CNN模型...")
    model = models.Sequential([
        # 第一卷积层：提取低级特征（边缘、线条）
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        
        # 第二卷积层：提取高级特征（曲线、形状）
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # 防止过拟合
        layers.Dropout(0.25),
        
        # 全连接层
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        
        # 输出层：10个数字类别
        layers.Dense(10, activation='softmax')
    ])
    
    return model

# 3. 可视化训练过程
def plot_training_history(history):
    """绘制训练过程中的准确率和损失曲线"""
    plt.figure(figsize=(12, 4))
    
    # 绘制准确率曲线
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='训练准确率')
    plt.plot(history.history['val_accuracy'], label='验证准确率')
    plt.title('模型准确率')
    plt.xlabel('训练轮次')
    plt.ylabel('准确率')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 绘制损失曲线
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='训练损失')
    plt.plot(history.history['val_loss'], label='验证损失')
    plt.title('模型损失')
    plt.xlabel('训练轮次')
    plt.ylabel('损失')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# 4. 可视化预测结果
def visualize_predictions(model, test_images, test_labels, num_samples=10):
    """可视化模型预测结果"""
    print("可视化预测结果...")
    
    # 随机选择一些测试样本
    indices = np.random.choice(len(test_images), num_samples, replace=False)
    sample_images = test_images[indices]
    sample_labels = test_labels[indices]
    
    # 进行预测
    predictions = model.predict(sample_images)
    predicted_labels = np.argmax(predictions, axis=1)
    
    # 创建可视化图表
    plt.figure(figsize=(12, 8))
    for i in range(num_samples):
        plt.subplot(2, 5, i+1)
        plt.imshow(sample_images[i].reshape(28, 28), cmap='gray')
        
        # 显示预测结果和真实标签
        color = 'green' if predicted_labels[i] == sample_labels[i] else 'red'
        plt.title(f'预测: {predicted_labels[i]}\n实际: {sample_labels[i]}', color=color)
        plt.axis('off')
    
    plt.suptitle('模型预测结果（绿色正确，红色错误）')
    plt.tight_layout()
    plt.show()

# 5. 主函数
def main():
    """主函数：执行完整的训练和评估流程"""
    # 加载数据
    (train_images, train_labels), (test_images, test_labels) = load_and_preprocess_data()
    
    # 创建模型
    model = create_cnn_model()
    
    # 编译模型
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    
    # 显示模型结构
    print("模型结构摘要:")
    model.summary()
    
    # 训练模型
    print("开始训练模型...")
    history = model.fit(train_images, train_labels,
                        epochs=10,
                        batch_size=128,
                        validation_split=0.2,
                        verbose=1)
    
    # 评估模型
    print("在测试集上评估模型...")
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=0)
    print(f'测试准确率: {test_acc:.4f}')
    print(f'测试损失: {test_loss:.4f}')
    
    # 可视化训练过程
    plot_training_history(history)
    
    # 可视化预测结果
    visualize_predictions(model, test_images, test_labels)
    
    # 保存模型
    model.save('mnist_cnn_model.h5')
    print("模型已保存为 'mnist_cnn_model.h5'")
    
    return model, history

# 6. 单独预测函数
def predict_single_image(model, image_path=None):
    """对单张图像进行预测"""
    if image_path:
        # 如果提供了图像路径，可以在这里添加加载和预处理自定义图像的代码
        pass
    else:
        # 使用测试集中的随机图像
        (_, _), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
        test_images = test_images.astype('float32') / 255
        
        # 随机选择一张图像
        idx = np.random.randint(0, len(test_images))
        image = test_images[idx]
        true_label = test_labels[idx]
        
        # 预处理图像（添加批次和通道维度）
        image_for_prediction = image.reshape(1, 28, 28, 1)
        
        # 进行预测
        prediction = model.predict(image_for_prediction)
        predicted_label = np.argmax(prediction, axis=1)[0]
        confidence = np.max(prediction)
        
        # 显示结果
        plt.figure(figsize=(6, 6))
        plt.imshow(image, cmap='gray')
        plt.title(f'预测: {predicted_label} (置信度: {confidence:.2%})\n实际: {true_label}')
        plt.axis('off')
        plt.show()
        
        return predicted_label, true_label, confidence

# 执行主函数
if __name__ == "__main__":
    # 运行完整流程
    trained_model, training_history = main()
    
    # 示例：对单张图像进行预测
    # predict_single_image(trained_model)