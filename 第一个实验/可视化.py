# import tensorflow as tf
# from tensorflow.keras import layers, models, Model
# from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Activation
# from tensorflow.keras.optimizers import SGD, Adam
# from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# import numpy as np
# import os
# import cv2
# from datetime import datetime
# import matplotlib.pyplot as plt
# import matplotlib.font_manager as fm
# import json

# # 设置中文字体显示
# def set_chinese_font():
#     """设置中文字体显示"""
#     try:
#         # 尝试使用系统中文字体
#         plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
#         plt.rcParams['axes.unicode_minus'] = False
#         print("中文字体设置成功")
#     except Exception as e:
#         print(f"警告: 中文字体设置失败: {e}，将使用默认字体")

# # 参数设置
# IMG_CHANNELS = 3  # RGB图像为三通道
# IMG_ROWS = 224   # 图像的行像素
# IMG_COLS = 224   # 图像的列像素
# BATCH_SIZE = 32  # batch大小，减小以适应内存
# NB_EPOCH = 10    # 循环次数
# NB_CLASSES = 2   # 分类：猫和狗两种

# # 创建保存目录
# def create_directories():
#     """创建必要的目录结构"""
#     directories = [
#         'weights',
#         'training_logs',
#         'visualizations'
#     ]
    
#     for directory in directories:
#         if not os.path.exists(directory):
#             os.makedirs(directory)
#             print(f"创建目录: {directory}")

# # 数据加载函数 - 从文件夹加载猫狗图片
# def load_data_from_folders(cat_folder, dog_folder, max_images_per_class=2500, test_split=0.2):
#     """
#     从猫和狗的文件夹加载图片
#     Args:
#         cat_folder: 猫图片文件夹路径
#         dog_folder: 狗图片文件夹路径
#         max_images_per_class: 每个类别最大图片数
#         test_split: 测试集比例
#     """
#     x_train = []
#     y_train = []
#     x_test = []
#     y_test = []
    
#     # 加载猫图片
#     cat_images_loaded = 0
#     if os.path.exists(cat_folder):
#         for filename in os.listdir(cat_folder)[:max_images_per_class]:
#             if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
#                 try:
#                     img_path = os.path.join(cat_folder, filename)
#                     img = cv2.imread(img_path)
#                     if img is not None:
#                         # 调整图像大小并转换颜色空间
#                         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#                         img = cv2.resize(img, (IMG_ROWS, IMG_COLS))
#                         img = img.astype(np.float32) / 255.0  # 归一化
                        
#                         # 按照比例划分训练集和测试集
#                         if cat_images_loaded < max_images_per_class * (1 - test_split):
#                             x_train.append(img)
#                             y_train.append(0)  # 猫的标签为0
#                         else:
#                             x_test.append(img)
#                             y_test.append(0)  # 猫的标签为0
                        
#                         cat_images_loaded += 1
#                         if cat_images_loaded >= max_images_per_class:
#                             break
#                 except Exception as e:
#                     print(f"加载猫图片 {filename} 时出错: {e}")
#     else:
#         print(f"警告: 猫文件夹 {cat_folder} 不存在!")
    
#     # 加载狗图片
#     dog_images_loaded = 0
#     if os.path.exists(dog_folder):
#         for filename in os.listdir(dog_folder)[:max_images_per_class]:
#             if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
#                 try:
#                     img_path = os.path.join(dog_folder, filename)
#                     img = cv2.imread(img_path)
#                     if img is not None:
#                         # 调整图像大小并转换颜色空间
#                         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#                         img = cv2.resize(img, (IMG_ROWS, IMG_COLS))
#                         img = img.astype(np.float32) / 255.0  # 归一化
                        
#                         # 按照比例划分训练集和测试集
#                         if dog_images_loaded < max_images_per_class * (1 - test_split):
#                             x_train.append(img)
#                             y_train.append(1)  # 狗的标签为1
#                         else:
#                             x_test.append(img)
#                             y_test.append(1)  # 狗的标签为1
                        
#                         dog_images_loaded += 1
#                         if dog_images_loaded >= max_images_per_class:
#                             break
#                 except Exception as e:
#                     print(f"加载狗图片 {filename} 时出错: {e}")
#     else:
#         print(f"警告: 狗文件夹 {dog_folder} 不存在!")
    
#     # 转换为numpy数组
#     if len(x_train) > 0:
#         x_train = np.array(x_train)
#         y_train = np.array(y_train)
#     else:
#         # 如果数据加载失败，使用随机数据
#         x_train = np.random.random((max_images_per_class * (1 - test_split), IMG_ROWS, IMG_COLS, 3)).astype(np.float32)
#         y_train = np.zeros(max_images_per_class * (1 - test_split))
    
#     if len(x_test) > 0:
#         x_test = np.array(x_test)
#         y_test = np.array(y_test)
#     else:
#         x_test = np.random.random((max_images_per_class * test_split, IMG_ROWS, IMG_COLS, 3)).astype(np.float32)
#         y_test = np.zeros(max_images_per_class * test_split)
    
#     # 转换为one-hot编码
#     y_train = to_categorical(y_train, NB_CLASSES)
#     y_test = to_categorical(y_test, NB_CLASSES)
    
#     print(f"训练数据: {x_train.shape}, 训练标签: {y_train.shape}")
#     print(f"测试数据: {x_test.shape}, 测试标签: {y_test.shape}")
#     print(f"猫图片加载: {np.sum(y_train[:,0] == 1) + np.sum(y_test[:,0] == 1)} 张")
#     print(f"狗图片加载: {np.sum(y_train[:,1] == 1) + np.sum(y_test[:,1] == 1)} 张")
    
#     return (x_train, y_train), (x_test, y_test)

# # AlexNet模型定义 - 修改为Sigmoid激活函数
# def alex_net(activation_func='sigmoid'):
#     """定义AlexNet模型"""
#     input_shape = (IMG_ROWS, IMG_COLS, IMG_CHANNELS)
    
#     # 输入层
#     inputs = Input(shape=input_shape, name='input')
    
#     # 第一层：卷积 + 池化
#     x = layers.ZeroPadding2D(((1, 2), (1, 2)))(inputs)  # 224x224 -> 227x227
#     x = Conv2D(96, (11, 11), strides=(4, 4), activation=activation_func, name='conv1')(x)
#     x = MaxPooling2D((3, 3), strides=(2, 2), name='pool1')(x)
    
#     # 第二层：卷积 + 池化
#     x = Conv2D(256, (5, 5), activation=activation_func, padding='same', name='conv2')(x)
#     x = MaxPooling2D((3, 3), strides=(2, 2), name='pool2')(x)
    
#     # 第三层：卷积
#     x = Conv2D(384, (3, 3), activation=activation_func, padding='same', name='conv3')(x)
    
#     # 第四层：卷积
#     x = Conv2D(384, (3, 3), activation=activation_func, padding='same', name='conv4')(x)
    
#     # 第五层：卷积 + 池化
#     x = Conv2D(256, (3, 3), activation=activation_func, padding='same', name='conv5')(x)
#     x = MaxPooling2D((3, 3), strides=(2, 2), name='pool3')(x)
    
#     # 展平
#     x = Flatten(name='flatten')(x)
    
#     # 全连接层 + Dropout
#     x = Dense(4096, activation=activation_func, name='fc1')(x)
#     x = Dropout(0.5)(x)
    
#     x = Dense(4096, activation=activation_func, name='fc2')(x)
#     x = Dropout(0.5)(x)
    
#     # 输出层
#     x = Dense(NB_CLASSES, name='output')(x)
#     outputs = Activation('softmax', name='softmax')(x)
    
#     model = Model(inputs=inputs, outputs=outputs, name='AlexNet')
    
#     return model

# # 创建回调函数
# def create_callbacks(experiment_name):
#     """创建训练回调函数"""
    
#     # 保存最佳模型
#     best_model_path = f"weights/best_{experiment_name}.keras"  # 使用新的Keras格式
#     checkpoint_best = ModelCheckpoint(
#         best_model_path,
#         monitor='val_accuracy',
#         verbose=1,
#         save_best_only=True,
#         mode='max'
#     )
    
#     # 早停法
#     early_stop = EarlyStopping(
#         monitor='val_accuracy',
#         patience=5,
#         restore_best_weights=True,
#         verbose=1
#     )
    
#     # 学习率调整
#     reduce_lr = ReduceLROnPlateau(
#         monitor='val_accuracy',
#         factor=0.5,
#         patience=3,
#         min_lr=1e-7,
#         verbose=1
#     )
    
#     return [checkpoint_best, early_stop, reduce_lr]

# # 绘制训练历史 - 增强中文字体支持
# def plot_training_history(history, experiment_name):
#     """绘制训练历史曲线"""
    
#     # 设置中文字体
#     set_chinese_font()
    
#     # 创建图表
#     plt.figure(figsize=(14, 6))
    
#     # 准确率曲线
#     plt.subplot(1, 2, 1)
#     plt.plot(history.history['accuracy'], 'b-', linewidth=2, label='训练准确率')
#     plt.plot(history.history['val_accuracy'], 'r-', linewidth=2, label='验证准确率')
#     plt.title(f'{experiment_name} - 准确率', fontsize=14, fontweight='bold')
#     plt.xlabel('训练轮次 (Epoch)')
#     plt.ylabel('准确率')
#     plt.legend()
#     plt.grid(True, alpha=0.3)
#     plt.ylim([0, 1])  # 准确率范围0-1
    
#     # 损失曲线
#     plt.subplot(1, 2, 2)
#     plt.plot(history.history['loss'], 'b-', linewidth=2, label='训练损失')
#     plt.plot(history.history['val_loss'], 'r-', linewidth=2, label='验证损失')
#     plt.title(f'{experiment_name} - 损失', fontsize=14, fontweight='bold')
#     plt.xlabel('训练轮次 (Epoch)')
#     plt.ylabel('损失值')
#     plt.legend()
#     plt.grid(True, alpha=0.3)
    
#     plt.tight_layout()
#     plt.savefig(f'visualizations/training_curves_{experiment_name}.png', 
#                 dpi=300, bbox_inches='tight', facecolor='white')
#     plt.show()
#     plt.close()

# # 训练函数 - 修改激活函数为Sigmoid，学习率为0.01
# def train_model():
#     """训练AlexNet模型"""
    
#     # 设置中文字体
#     set_chinese_font()
    
#     # 创建目录
#     create_directories()
    
#     print("开始训练AlexNet猫狗分类模型...")
#     print(f"图像尺寸: {IMG_ROWS}x{IMG_COLS}")
#     print(f"批次大小: {BATCH_SIZE}")
#     print(f"训练轮数: {NB_EPOCH}")
#     print(f"学习率: 0.01")
#     print(f"激活函数: Sigmoid (已修改)")
    
#     # 请修改为您的实际路径
#     cat_folder = "F:/data/PetImages/Cat"  # 猫图片文件夹路径
#     dog_folder = "F:/data/PetImages/Dog"  # 狗图片文件夹路径
    
#     # 加载数据
#     print("加载数据中...")
#     (x_train, y_train), (x_test, y_test) = load_data_from_folders(cat_folder, dog_folder)
    
#     # 如果数据加载失败，使用随机数据（用于测试）
#     if len(x_train) == 0:
#         print("无法从文件夹加载数据，使用随机数据用于演示...")
#         x_train = np.random.random((800, IMG_ROWS, IMG_COLS, 3)).astype(np.float32)
#         x_test = np.random.random((200, IMG_ROWS, IMG_COLS, 3)).astype(np.float32)
#         y_train = to_categorical(np.random.randint(0, 2, 800), NB_CLASSES)
#         y_test = to_categorical(np.random.randint(0, 2, 200), NB_CLASSES)
    
#     # 创建模型 - 修改为Sigmoid激活函数
#     print("创建AlexNet模型（使用Sigmoid激活函数）...")
#     model = alex_net(activation_func='sigmoid')
    
#     # 编译模型 - 学习率保持0.01
#     sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
#     model.compile(
#         loss='categorical_crossentropy',
#         optimizer=sgd,
#         metrics=['accuracy']
#     )
    
#     # 显示模型结构
#     model.summary()
    
#     # 创建回调函数 - 修改实验名称以反映激活函数变化
#     callbacks = create_callbacks('alexnet_cat_dog_sigmoid_lr0.01')
    
#     print("开始训练...")
#     # 训练模型
#     history = model.fit(
#         x_train, y_train,
#         batch_size=BATCH_SIZE,
#         epochs=NB_EPOCH,
#         verbose=1,
#         validation_data=(x_test, y_test),
#         callbacks=callbacks
#     )
    
#     # 评估模型
#     test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
#     print(f"测试准确率: {test_accuracy:.4f}, 测试损失: {test_loss:.4f}")
    
#     # 保存最终模型 - 修改文件名以反映激活函数
#     final_model_path = "weights/alexnet_cat_dog_sigmoid_lr0.01_final.keras"
#     model.save(final_model_path)
#     print(f"最终模型已保存: {final_model_path}")
    
#     # 绘制训练曲线 - 修改实验名称
#     plot_training_history(history, 'AlexNet_Sigmoid_lr0.01')
    
#     # 保存训练历史
#     history_dict = {
#         'accuracy': [float(x) for x in history.history['accuracy']],
#         'val_accuracy': [float(x) for x in history.history['val_accuracy']],
#         'loss': [float(x) for x in history.history['loss']],
#         'val_loss': [float(x) for x in history.history['val_loss']],
#         'test_accuracy': float(test_accuracy),
#         'test_loss': float(test_loss),
#         'learning_rate': 0.01,
#         'activation_function': 'sigmoid',
#         'timestamp': datetime.now().isoformat()
#     }
    
#     # 保存为JSON - 修改文件名
#     history_path = "training_logs/training_history_sigmoid_lr0.01.json"
#     with open(history_path, 'w', encoding='utf-8') as f:
#         json.dump(history_dict, f, indent=2, ensure_ascii=False)
#     print(f"训练历史已保存: {history_path}")
    
#     return model, history

# # 主函数
# def main():
#     """主执行函数"""
#     try:
#         model, history = train_model()
#         print("\n训练完成！")
#         print("生成的文件:")
#         print("- weights/best_alexnet_cat_dog_sigmoid_lr0.01.keras (最佳模型)")
#         print("- weights/alexnet_cat_dog_sigmoid_lr0.01_final.keras (最终模型)")
#         print("- visualizations/training_curves_AlexNet_Sigmoid_lr0.01.png (训练曲线)")
#         print("- training_logs/training_history_sigmoid_lr0.01.json (训练历史)")
        
#     except Exception as e:
#         print(f"训练过程中出现错误: {e}")
#         import traceback
#         traceback.print_exc()

# if __name__ == "__main__":
#     main()


import tensorflow as tf
from tensorflow.keras import layers, models, Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Activation
from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator
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
        # 尝试使用系统中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        print("中文字体设置成功")
    except Exception as e:
        print(f"警告: 中文字体设置失败: {e}，将使用默认字体")

# 参数设置
IMG_CHANNELS = 3  # RGB图像为三通道
IMG_ROWS = 224   # 图像的行像素
IMG_COLS = 224   # 图像的列像素
BATCH_SIZE = 32  # batch大小
NB_EPOCH = 100  # 大幅增加循环次数到100轮
NB_CLASSES = 2   # 分类：猫和狗两种

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

# 数据加载函数 - 从文件夹加载猫狗图片
def load_data_from_folders(cat_folder, dog_folder, max_images_per_class=2500, test_split=0.1):
    """
    从猫和狗的文件夹加载图片
    Args:
        cat_folder: 猫图片文件夹路径
        dog_folder: 狗图片文件夹路径
        max_images_per_class: 每个类别最大图片数
        test_split: 测试集比例
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
                        # 调整图像大小并转换颜色空间
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (IMG_ROWS, IMG_COLS))
                        img = img.astype(np.float32) / 255.0  # 归一化
                        
                        # 按照比例划分训练集和测试集
                        if cat_images_loaded < max_images_per_class * (1 - test_split):
                            x_train.append(img)
                            y_train.append(0)  # 猫的标签为0
                        else:
                            x_test.append(img)
                            y_test.append(0)  # 猫的标签为0
                        
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
                        # 调整图像大小并转换颜色空间
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img = cv2.resize(img, (IMG_ROWS, IMG_COLS))
                        img = img.astype(np.float32) / 255.0  # 归一化
                        
                        # 按照比例划分训练集和测试集
                        if dog_images_loaded < max_images_per_class * (1 - test_split):
                            x_train.append(img)
                            y_train.append(1)  # 狗的标签为1
                        else:
                            x_test.append(img)
                            y_test.append(1)  # 狗的标签为1
                        
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
        # 如果数据加载失败，使用随机数据
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
    print(f"猫图片加载: {np.sum(y_train[:,0] == 1) + np.sum(y_test[:,0] == 1)} 张")
    print(f"狗图片加载: {np.sum(y_train[:,1] == 1) + np.sum(y_test[:,1] == 1)} 张")
    
    return (x_train, y_train), (x_test, y_test)

# AlexNet模型定义 - 修改为Softsign激活函数
def alex_net():
    """定义AlexNet模型（使用Softsign激活函数）"""
    input_shape = (IMG_ROWS, IMG_COLS, IMG_CHANNELS)
    
    # 输入层
    inputs = Input(shape=input_shape, name='input')
    
    # 第一层：卷积 + 池化
    x = layers.ZeroPadding2D(((1, 2), (1, 2)))(inputs)  # 224x224 -> 227x227
    x = Conv2D(96, (11, 11), strides=(4, 4), activation='softsign', name='conv1')(x)
    x = MaxPooling2D((3, 3), strides=(2, 2), name='pool1')(x)
    
    # 第二层：卷积 + 池化
    x = Conv2D(256, (5, 5), activation='softsign', padding='same', name='conv2')(x)
    x = MaxPooling2D((3, 3), strides=(2, 2), name='pool2')(x)
    
    # 第三层：卷积
    x = Conv2D(384, (3, 3), activation='softsign', padding='same', name='conv3')(x)
    
    # 第四层：卷积
    x = Conv2D(384, (3, 3), activation='softsign', padding='same', name='conv4')(x)
    
    # 第五层：卷积 + 池化
    x = Conv2D(256, (3, 3), activation='softsign', padding='same', name='conv5')(x)
    x = MaxPooling2D((3, 3), strides=(2, 2), name='pool3')(x)
    
    # 展平
    x = Flatten(name='flatten')(x)
    
    # 全连接层 + Dropout
    x = Dense(4096, activation='softsign', name='fc1')(x)
    x = Dropout(0.5)(x)
    
    x = Dense(4096, activation='softsign', name='fc2')(x)
    x = Dropout(0.5)(x)
    
    # 输出层（保持softmax用于分类）
    x = Dense(NB_CLASSES, name='output')(x)
    outputs = Activation('softmax', name='softmax')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name='AlexNet_Softsign')
    
    return model

# 创建数据增强生成器
def create_data_augmentation():
    """创建数据增强生成器，这对于小数据集特别重要"""
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        fill_mode='nearest'
    )
    return datagen

# 创建回调函数 - 优化EarlyStopping参数
def create_callbacks(experiment_name):
    """创建训练回调函数"""
    
    # 保存最佳模型
    best_model_path = f"weights/best_{experiment_name}.keras"
    checkpoint_best = ModelCheckpoint(
        best_model_path,
        monitor='val_accuracy',
        verbose=1,
        save_best_only=True,
        mode='max'
    )
    
    # 早停法 - 大幅增加patience值，避免过早停止
    early_stop = EarlyStopping(
        monitor='val_accuracy',
        patience=30,  # 从5增加到30，给予模型更多训练时间
        min_delta=0.001,  # 设置最小改善阈值
        restore_best_weights=True,
        verbose=1,
        mode='max'
    )
    
    # 学习率调整 - 改为监控验证损失
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',  # 改为监控验证损失
        factor=0.5,
        patience=10,  # 增加耐心值
        min_lr=1e-7,
        verbose=1
    )
    
    return [checkpoint_best, early_stop, reduce_lr]

# 绘制训练历史 - 增强中文字体支持
def plot_training_history(history, experiment_name):
    """绘制训练历史曲线"""
    
    # 设置中文字体
    set_chinese_font()
    
    # 创建图表
    plt.figure(figsize=(14, 6))
    
    # 准确率曲线
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], 'b-', linewidth=2, label='训练准确率')
    plt.plot(history.history['val_accuracy'], 'r-', linewidth=2, label='验证准确率')
    plt.title(f'{experiment_name} - 准确率', fontsize=14, fontweight='bold')
    plt.xlabel('训练轮次 (Epoch)')
    plt.ylabel('准确率')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim([0, 1])
    
    # 损失曲线
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], 'b-', linewidth=2, label='训练损失')
    plt.plot(history.history['val_loss'], 'r-', linewidth=2, label='验证损失')
    plt.title(f'{experiment_name} - 损失', fontsize=14, fontweight='bold')
    plt.xlabel('训练轮次 (Epoch)')
    plt.ylabel('损失值')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'visualizations/training_curves_{experiment_name}.png', 
                dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    plt.close()

# 训练函数 - 使用Softsign激活函数
def train_model():
    """训练AlexNet模型（使用Softsign激活函数）"""
    
    # 设置中文字体
    set_chinese_font()
    
    # 创建目录
    create_directories()
    
    print("开始训练AlexNet猫狗分类模型...")
    print(f"图像尺寸: {IMG_ROWS}x{IMG_COLS}")
    print(f"批次大小: {BATCH_SIZE}")
    print(f"训练轮数: {NB_EPOCH}")
    print(f"学习率: 0.001 (Adam优化器)")
    print(f"激活函数: Softsign (平滑的S型激活函数)")
    print(f"早停耐心值: 30 (大幅增加以避免过早停止)")
    
    # 请修改为您的实际路径
    cat_folder = "F:/data/PetImages/Cat"  # 猫图片文件夹路径
    dog_folder = "F:/data/PetImages/Dog"  # 狗图片文件夹路径
    
    # 加载数据
    print("加载数据中...")
    (x_train, y_train), (x_test, y_test) = load_data_from_folders(cat_folder, dog_folder)
    
    # 如果数据加载失败，使用随机数据（用于测试）
    if len(x_train) == 0:
        print("无法从文件夹加载数据，使用随机数据用于演示...")
        x_train = np.random.random((800, IMG_ROWS, IMG_COLS, 3)).astype(np.float32)
        x_test = np.random.random((200, IMG_ROWS, IMG_COLS, 3)).astype(np.float32)
        y_train = to_categorical(np.random.randint(0, 2, 800), NB_CLASSES)
        y_test = to_categorical(np.random.randint(0, 2, 200), NB_CLASSES)
    
    # 创建数据增强 - 这对于小数据集特别重要
    print("创建数据增强生成器...")
    datagen = create_data_augmentation()
    
    # 创建模型 - 使用Softsign激活函数
    print("创建AlexNet模型（使用Softsign激活函数）...")
    model = alex_net()
    
    # 编译模型 - 使用Adam优化器和更小的学习率
    optimizer = Adam(learning_rate=0.001)
    model.compile(
        loss='categorical_crossentropy',
        optimizer=optimizer,
        metrics=['accuracy']
    )
    
    # 显示模型结构
    model.summary()
    
    # 创建回调函数
    experiment_name = 'alexnet_cat_dog_softsign'
    callbacks = create_callbacks(experiment_name)
    
    print("开始训练...")
    # 训练模型（使用数据增强）
    history = model.fit(
        datagen.flow(x_train, y_train, batch_size=BATCH_SIZE),
        steps_per_epoch=len(x_train) // BATCH_SIZE,
        epochs=NB_EPOCH,
        verbose=1,
        validation_data=(x_test, y_test),
        callbacks=callbacks
    )
    
    # 评估模型
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"测试准确率: {test_accuracy:.4f}, 测试损失: {test_loss:.4f}")
    
    # 保存最终模型
    final_model_path = f"weights/{experiment_name}_final.keras"
    model.save(final_model_path)
    print(f"最终模型已保存: {final_model_path}")
    
    # 绘制训练曲线
    plot_training_history(history, 'AlexNet_Softsign_Training')
    
    # 保存训练历史
    actual_epochs = len(history.history['accuracy'])
    history_dict = {
        'accuracy': [float(x) for x in history.history['accuracy']],
        'val_accuracy': [float(x) for x in history.history['val_accuracy']],
        'loss': [float(x) for x in history.history['loss']],
        'val_loss': [float(x) for x in history.history['val_loss']],
        'test_accuracy': float(test_accuracy),
        'test_loss': float(test_loss),
        'learning_rate': 0.001,
        'activation_function': 'softsign',
        'optimizer': 'adam',
        'timestamp': datetime.now().isoformat(),
        'actual_epochs_trained': actual_epochs,
        'max_epochs': NB_EPOCH,
        'early_stopping_patience': 30
    }
    
    # 保存为JSON
    history_path = f"training_logs/training_history_{experiment_name}.json"
    with open(history_path, 'w', encoding='utf-8') as f:
        json.dump(history_dict, f, indent=2, ensure_ascii=False)
    print(f"训练历史已保存: {history_path}")
    
    # 打印详细的训练信息
    actual_epochs = len(history.history['accuracy'])
    print(f"\n=== 训练总结 ===")
    print(f"计划训练轮次: {NB_EPOCH}")
    print(f"实际训练轮次: {actual_epochs}")
    print(f"早停触发: {'是' if actual_epochs < NB_EPOCH else '否'}")
    print(f"最终测试准确率: {test_accuracy:.4f}")
    print(f"使用的激活函数: Softsign")
    
    return model, history

# 主函数
def main():
    """主执行函数"""
    try:
        model, history = train_model()
        print("\n训练完成！")
        actual_epochs = len(history.history['accuracy'])
        print(f"实际训练轮次: {actual_epochs}")
        print("生成的文件:")
        print("- weights/best_alexnet_cat_dog_softsign.keras (最佳模型)")
        print("- weights/alexnet_cat_dog_softsign_final.keras (最终模型)")
        print("- visualizations/training_curves_AlexNet_Softsign_Training.png (训练曲线)")
        print("- training_logs/training_history_alexnet_cat_dog_softsign.json (训练历史)")
        
    except Exception as e:
        print(f"训练过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()