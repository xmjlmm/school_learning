import tensorflow as tf
from tensorflow.keras import layers, models, Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Activation, BatchNormalization
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.initializers import HeNormal, GlorotUniform
import numpy as np
import os
import cv2
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import json

# 设置中文字体显示
def set_chinese_font():
    """设置中文字体显示"""
    try:
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        print("中文字体设置成功")
    except Exception as e:
        print(f"警告: 中文字体设置失败: {e}，将使用默认字体")

# 参数设置
IMG_CHANNELS = 3
IMG_ROWS = 224
IMG_COLS = 224
BATCH_SIZE = 32
NB_EPOCH = 100
NB_CLASSES = 2

# 创建保存目录
def create_directories():
    """创建必要的目录结构"""
    directories = [
        'weights',
        'training_logs', 
        'visualizations'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"创建目录: {directory}")

# 数据加载函数
def load_data_from_folders(cat_folder, dog_folder, max_images_per_class=2500, test_split=0.2):
    """
    从猫和狗的文件夹加载图片
    """
    x_train = []
    y_train = []
    x_test = []
    y_test = []
    
    # 加载猫图片
    cat_images_loaded = 0
    if os.path.exists(cat_folder):
        for filename in os.listdir(cat_folder)[:max_images_per_class]:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                try:
                    img_path = os.path.join(cat_folder, filename)
                    img = cv2.imread(img_path)
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (IMG_ROWS, IMG_COLS))
                        img = img.astype(np.float32) / 255.0
                        
                        if cat_images_loaded < max_images_per_class * (1 - test_split):
                            x_train.append(img)
                            y_train.append(0)
                        else:
                            x_test.append(img)
                            y_test.append(0)
                        
                        cat_images_loaded += 1
                        if cat_images_loaded >= max_images_per_class:
                            break
                except Exception as e:
                    print(f"加载猫图片 {filename} 时出错: {e}")
    else:
        print(f"警告: 猫文件夹 {cat_folder} 不存在!")
    
    # 加载狗图片
    dog_images_loaded = 0
    if os.path.exists(dog_folder):
        for filename in os.listdir(dog_folder)[:max_images_per_class]:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                try:
                    img_path = os.path.join(dog_folder, filename)
                    img = cv2.imread(img_path)
                    if img is not None:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (IMG_ROWS, IMG_COLS))
                        img = img.astype(np.float32) / 255.0
                        
                        if dog_images_loaded < max_images_per_class * (1 - test_split):
                            x_train.append(img)
                            y_train.append(1)
                        else:
                            x_test.append(img)
                            y_test.append(1)
                        
                        dog_images_loaded += 1
                        if dog_images_loaded >= max_images_per_class:
                            break
                except Exception as e:
                    print(f"加载狗图片 {filename} 时出错: {e}")
    else:
        print(f"警告: 狗文件夹 {dog_folder} 不存在!")
    
    # 转换为numpy数组
    if len(x_train) > 0:
        x_train = np.array(x_train)
        y_train = np.array(y_train)
    else:
        x_train = np.random.random((max_images_per_class * (1 - test_split), IMG_ROWS, IMG_COLS, 3)).astype(np.float32)
        y_train = np.zeros(max_images_per_class * (1 - test_split))
    
    if len(x_test) > 0:
        x_test = np.array(x_test)
        y_test = np.array(y_test)
    else:
        x_test = np.random.random((max_images_per_class * test_split, IMG_ROWS, IMG_COLS, 3)).astype(np.float32)
        y_test = np.zeros(max_images_per_class * test_split)
    
    # 转换为one-hot编码
    y_train = to_categorical(y_train, NB_CLASSES)
    y_test = to_categorical(y_test, NB_CLASSES)
    
    print(f"训练数据: {x_train.shape}, 训练标签: {y_train.shape}")
    print(f"测试数据: {x_test.shape}, 测试标签: {y_test.shape}")
    
    return (x_train, y_train), (x_test, y_test)

# 改进的AlexNet模型 - 专门为Softsign优化
def improved_alex_net():
    """定义专门为Softsign优化的AlexNet模型"""
    input_shape = (IMG_ROWS, IMG_COLS, IMG_CHANNELS)
    
    # 使用更适合Softsign的初始化
    kernel_initializer = HeNormal()  # 使用He初始化替代默认初始化
    
    inputs = Input(shape=input_shape, name='input')
    
    # 第一层：卷积 + 批归一化 + Softsign + 池化
    x = layers.ZeroPadding2D(((1, 2), (1, 2)))(inputs)
    x = Conv2D(96, (11, 11), strides=(4, 4), padding='valid', 
               kernel_initializer=kernel_initializer, name='conv1')(x)
    x = BatchNormalization()(x)  # 添加批归一化
    x = Activation('softsign')(x)  # 在批归一化后使用Softsign
    x = MaxPooling2D((3, 3), strides=(2, 2), name='pool1')(x)
    
    # 第二层：卷积 + 批归一化 + Softsign + 池化
    x = Conv2D(256, (5, 5), padding='same', 
               kernel_initializer=kernel_initializer, name='conv2')(x)
    x = BatchNormalization()(x)
    x = Activation('softsign')(x)
    x = MaxPooling2D((3, 3), strides=(2, 2), name='pool2')(x)
    
    # 第三层：卷积 + 批归一化 + Softsign
    x = Conv2D(384, (3, 3), padding='same', 
               kernel_initializer=kernel_initializer, name='conv3')(x)
    x = BatchNormalization()(x)
    x = Activation('softsign')(x)
    
    # 第四层：卷积 + 批归一化 + Softsign
    x = Conv2D(384, (3, 3), padding='same', 
               kernel_initializer=kernel_initializer, name='conv4')(x)
    x = BatchNormalization()(x)
    x = Activation('softsign')(x)
    
    # 第五层：卷积 + 批归一化 + Softsign + 池化
    x = Conv2D(256, (3, 3), padding='same', 
               kernel_initializer=kernel_initializer, name='conv5')(x)
    x = BatchNormalization()(x)
    x = Activation('softsign')(x)
    x = MaxPooling2D((3, 3), strides=(2, 2), name='pool3')(x)
    
    # 展平
    x = Flatten(name='flatten')(x)
    
    # 全连接层1 + 批归一化 + Softsign + Dropout
    x = Dense(4096, kernel_initializer=kernel_initializer, name='fc1')(x)
    x = BatchNormalization()(x)
    x = Activation('softsign')(x)
    x = Dropout(0.3)(x)  # 降低Dropout比例
    
    # 全连接层2 + 批归一化 + Softsign + Dropout  
    x = Dense(4096, kernel_initializer=kernel_initializer, name='fc2')(x)
    x = BatchNormalization()(x)
    x = Activation('softsign')(x)
    x = Dropout(0.3)(x)  # 降低Dropout比例
    
    # 输出层
    x = Dense(NB_CLASSES, name='output')(x)
    outputs = Activation('softmax', name='softmax')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name='Improved_AlexNet_Softsign')
    return model

# 创建数据增强生成器
def create_data_augmentation():
    """创建数据增强生成器"""
    datagen = ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
        zoom_range=0.1,
        fill_mode='nearest'
    )
    return datagen

# 创建专门为Softsign优化的回调函数
def create_callbacks_softsign(experiment_name):
    """为Softsign激活函数创建专门的回调函数"""
    
    best_model_path = f"weights/best_{experiment_name}.keras"
    checkpoint_best = ModelCheckpoint(
        best_model_path,
        monitor='val_accuracy',
        verbose=1,
        save_best_only=True,
        mode='max'
    )
    
    # 为Softsign调整早停策略
    early_stop = EarlyStopping(
        monitor='val_accuracy',
        patience=20,  # 适当减少耐心值
        min_delta=0.0005,  # 更小的改善阈值
        restore_best_weights=True,
        verbose=1
    )
    
    # 更积极的学习率调整策略
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=8,  # 减少耐心值以更频繁调整
        min_lr=1e-6,
        verbose=1
    )
    
    return [checkpoint_best, early_stop, reduce_lr]

# 绘制训练历史
def plot_training_history(history, experiment_name):
    """绘制训练历史曲线"""
    set_chinese_font()
    
    plt.figure(figsize=(14, 6))
    
    # 准确率曲线
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], 'b-', linewidth=2, label='训练准确率')
    plt.plot(history.history['val_accuracy'], 'r-', linewidth=2, label='验证准确率')
    plt.title(f'{experiment_name} - 准确率', fontsize=14, fontweight='bold')
    plt.xlabel('训练轮次')
    plt.ylabel('准确率')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim([0, 1])
    
    # 损失曲线
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], 'b-', linewidth=2, label='训练损失')
    plt.plot(history.history['val_loss'], 'r-', linewidth=2, label='验证损失')
    plt.title(f'{experiment_name} - 损失', fontsize=14, fontweight='bold')
    plt.xlabel('训练轮次')
    plt.ylabel('损失值')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'visualizations/training_curves_{experiment_name}.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    plt.close()

# 专门为Softsign优化的训练函数
def train_softsign_model():
    """训练使用Softsign激活函数的AlexNet模型"""
    
    set_chinese_font()
    create_directories()
    
    print("开始训练使用Softsign激活函数的AlexNet模型")
    print("=" * 60)
    print(f"图像尺寸: {IMG_ROWS}x{IMG_COLS}")
    print(f"批次大小: {BATCH_SIZE}")
    print(f"最大训练轮数: {NB_EPOCH}")
    print(f"激活函数: Softsign (经过专门优化)")
    print(f"优化策略: 带梯度裁剪的Adam优化器")
    print("=" * 60)
    
    # 数据路径 - 请修改为您的实际路径
    cat_folder = "F:/data/PetImages/Cat"
    dog_folder = "F:/data/PetImages/Dog"
    
    # 加载数据
    print("加载数据中...")
    (x_train, y_train), (x_test, y_test) = load_data_from_folders(cat_folder, dog_folder)
    
    # 数据检查
    if len(x_train) == 0:
        print("无法从文件夹加载数据，使用随机数据用于演示...")
        x_train = np.random.random((800, IMG_ROWS, IMG_COLS, 3)).astype(np.float32)
        x_test = np.random.random((200, IMG_ROWS, IMG_COLS, 3)).astype(np.float32)
        y_train = to_categorical(np.random.randint(0, 2, 800), NB_CLASSES)
        y_test = to_categorical(np.random.randint(0, 2, 200), NB_CLASSES)
    
    print(f"训练样本数: {len(x_train)}")
    print(f"测试样本数: {len(x_test)}")
    
    # 创建数据增强
    datagen = create_data_augmentation()
    
    # 创建改进的模型
    print("创建改进的AlexNet模型（专为Softsign优化）...")
    model = improved_alex_net()
    
    # 为Softsign专门设计的优化器配置
    optimizer = Adam(
        learning_rate=0.001,  # 稍大的初始学习率
        beta_1=0.9,
        beta_2=0.999,
        epsilon=1e-7,
        clipvalue=1.0  # 梯度裁剪防止梯度爆炸
    )
    
    model.compile(
        loss='categorical_crossentropy',
        optimizer=optimizer,
        metrics=['accuracy']
    )
    
    # 显示模型结构
    model.summary()
    
    # 创建回调函数
    experiment_name = 'alexnet_softsign_optimized'
    callbacks = create_callbacks_softsign(experiment_name)
    
    print("开始训练...")
    # 训练模型
    history = model.fit(
        datagen.flow(x_train, y_train, batch_size=BATCH_SIZE),
        steps_per_epoch=len(x_train) // BATCH_SIZE,
        epochs=NB_EPOCH,
        verbose=1,
        validation_data=(x_test, y_test),
        callbacks=callbacks,
        shuffle=True
    )
    
    # 评估模型
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"最终测试准确率: {test_accuracy:.4f}")
    print(f"最终测试损失: {test_loss:.4f}")
    
    # 保存模型
    final_model_path = f"weights/{experiment_name}_final.keras"
    model.save(final_model_path)
    print(f"模型已保存: {final_model_path}")
    
    # 绘制训练曲线
    plot_training_history(history, 'AlexNet_Softsign_Optimized')
    
    # 保存训练历史
    actual_epochs = len(history.history['accuracy'])
    history_dict = {
        'accuracy': [float(x) for x in history.history['accuracy']],
        'val_accuracy': [float(x) for x in history.history['val_accuracy']],
        'loss': [float(x) for x in history.history['loss']],
        'val_loss': [float(x) for x in history.history['val_loss']],
        'test_accuracy': float(test_accuracy),
        'test_loss': float(test_loss),
        'final_learning_rate': float(optimizer.learning_rate.numpy()),
        'activation_function': 'softsign',
        'optimizer': 'adam_with_clipping',
        'batch_normalization': True,
        'timestamp': datetime.now().isoformat(),
        'actual_epochs_trained': actual_epochs
    }
    
    history_path = f"training_logs/training_history_{experiment_name}.json"
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history_dict, f, indent=2, ensure_ascii=False)
    print(f"训练历史已保存: {history_path}")
    
    # 训练总结
    print("\n" + "=" * 60)
    print("训练总结:")
    print(f"实际训练轮次: {actual_epochs}/{NB_EPOCH}")
    print(f"早停触发: {'是' if actual_epochs < NB_EPOCH else '否'}")
    print(f"最终测试准确率: {test_accuracy:.4f}")
    print(f"使用的激活函数: Softsign")
    print("主要改进措施:")
    print("- 添加了BatchNormalization层")
    print("- 使用了梯度裁剪")
    print("- 降低了Dropout比例")
    print("- 优化了学习率策略")
    print("=" * 60)
    
    return model, history

# 主函数
def main():
    """主执行函数"""
    try:
        print("Softsign优化版AlexNet猫狗分类模型")
        print("备注: 此版本专门针对Softsign激活函数的特性进行了优化")
        
        model, history = train_softsign_model()
        
        print("\n训练完成！")
        print("生成的文件清单:")
        print("- weights/best_alexnet_softsign_optimized.keras (最佳模型)")
        print("- weights/alexnet_softsign_optimized_final.keras (最终模型)") 
        print("- visualizations/training_curves_AlexNet_Softsign_Optimized.png (训练曲线)")
        print("- training_logs/training_history_alexnet_softsign_optimized.json (训练历史)")
        
    except Exception as e:
        print(f"训练过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()