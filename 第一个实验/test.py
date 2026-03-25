import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Activation, concatenate
import os

# 定义AlexNet模型结构（保持与训练时一致）
def alex_net():
    input_shape = (224, 224, 3)
    inputs = Input(shape=input_shape, name='input')
    
    # 第一层：卷积+池化
    x = Conv2D(96, (11, 11), strides=(4, 4), activation='relu', padding='same')(inputs)
    x = MaxPooling2D((3, 3), strides=(2, 2))(x)
    
    # 第二层：卷积+池化
    x = Conv2D(256, (5, 5), activation='relu', padding='same')(x)
    x = MaxPooling2D((3, 3), strides=(2, 2))(x)
    
    # 第三层：卷积
    x = Conv2D(384, (3, 3), activation='relu', padding='same')(x)
    
    # 第四层：卷积
    x = Conv2D(384, (3, 3), activation='relu', padding='same')(x)
    
    # 第五层：卷积+池化
    x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((3, 3), strides=(2, 2))(x)
    
    # 展平
    x = Flatten()(x)
    
    # 全连接层
    x = Dense(4096, activation='relu')(x)
    x = Dropout(0.5)(x)
    
    x = Dense(4096, activation='relu')(x)
    x = Dropout(0.5)(x)
    
    # 输出层
    x = Dense(2)(x)  # 2个输出节点：猫和狗
    outputs = Activation('softmax')(x)
    
    model = Model(inputs=inputs, outputs=outputs)
    return model

# 创建模型实例
AlexNet = alex_net()

# 加载权重文件
weights_path = "F:/PycharmProjects/weights/best_alexnet_cat_dog.h5"

if os.path.exists(weights_path):
    AlexNet.load_weights(weights_path)
    print("权重文件加载成功！")
else:
    print(f"警告：权重文件 {weights_path} 不存在！")
    # 编译模型（即使没有预训练权重也可以运行）
    AlexNet.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 图像预处理和预测
input_shape = (224, 224, 3)
img_path = r"F:/data/PetImages/Cat/5609.jpg"  # 待预测图片的路径

try:
    # 加载和预处理图像
    img = image.load_img(img_path, target_size=input_shape[0:2])  # 加载图像
    x = image.img_to_array(img)  # 转换为数组形式
    x = np.expand_dims(x, axis=0)  # 扩展维度为 (1, 224, 224, 3)
    x = x / 255.0  # 归一化
    
    # 进行预测
    pres = AlexNet.predict(x)
    print("预测结果形状:", pres.shape)
    print("预测值:", pres)
    
    # 修正标签解释：索引0对应猫，索引1对应狗
    # 这是最常见的设置方式[1,3](@ref)
    cat_prob = pres[0, 0]  # 索引0对应猫的概率
    dog_prob = pres[0, 1]  # 索引1对应狗的概率
    
    print(f"猫的概率: {cat_prob:.4f}")
    print(f"狗的概率: {dog_prob:.4f}")
    
    # 根据预测值判断类别
    if cat_prob > dog_prob:
        print("预测结果: 猫")
    else:
        print("预测结果: 狗")
        
except Exception as e:
    print(f"预测过程中出现错误: {e}")
    print("请检查图像路径是否正确，以及图像文件是否完好")

# 显示模型摘要
print("\n模型结构摘要:")
AlexNet.summary()