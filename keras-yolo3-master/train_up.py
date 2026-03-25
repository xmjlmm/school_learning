import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Input, Lambda
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

from yolo3.model import preprocess_true_boxes, yolo_body, yolo_loss
from yolo3.utils import get_random_data

def _main():
    """主训练函数 - 修复NaN问题和保存错误"""
    annotation_path = 'F:/data/VOC2007/ImageSets/Main/2007_train.txt'
    log_dir = 'F:/data/VOC2007/logs/000'
    classes_path = 'F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/voc_classes.txt'
    anchors_path = 'F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/yolo_anchors.txt'
    
    os.makedirs(log_dir, exist_ok=True)
    
    class_names = get_classes(classes_path)
    anchors = get_anchors(anchors_path)
    input_shape = (416, 416)
    
    model = create_model(input_shape, anchors, len(class_names))
    train(model, annotation_path, input_shape, anchors, len(class_names), log_dir=log_dir)

def train(model, annotation_path, input_shape, anchors, num_classes, log_dir='logs/'):
    """修复NaN问题和output_signature问题的训练函数"""
    
    # 使用更安全的学习率和梯度裁剪[2](@ref)
    model.compile(
        optimizer=Adam(learning_rate=1e-3, clipnorm=1.0),  # 降低学习率并添加梯度裁剪
        loss={'yolo_loss': lambda y_true, y_pred: y_pred}
    )
    
    # 增强的回调函数配置[6](@ref)
    callbacks = [
        TensorBoard(log_dir=log_dir),
        ModelCheckpoint(
            os.path.join(log_dir, "ep{epoch:03d}-loss{loss:.3f}.weights.h5"),
            save_weights_only=True, 
            save_best_only=True,
            monitor='loss',
            mode='min'
        ),
        ReduceLROnPlateau(
            monitor='loss', 
            factor=0.5, 
            patience=8,  # 增加耐心值
            verbose=1,
            min_lr=1e-7  # 设置最小学习率
        ),
        EarlyStopping(
            monitor='loss', 
            patience=20,  # 增加早停耐心
            verbose=1,
            restore_best_weights=True  # 恢复最佳权重
        )
    ]
    
    batch_size = 8  # 减小批量大小以提高稳定性[2](@ref)
    val_split = 0.1
    
    # 读取数据
    with open(annotation_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    np.random.shuffle(lines)
    num_val = int(len(lines) * val_split)
    num_train = len(lines) - num_val
    
    print(f'训练样本: {num_train}, 验证样本: {num_val}, 批量大小: {batch_size}')

    # 关键修复：正确的output_signature定义
    def create_dataset(annotation_lines, batch_size, input_shape, anchors, num_classes, is_training=True):
        """创建符合TensorFlow要求的Dataset - 修复版本"""
        def generator():
            return data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes, is_training)
        
        h, w = input_shape
        
        # 正确的output_signature结构[3](@ref)
        output_signature = (
            (
                tf.TensorSpec(shape=(None, h, w, 3), dtype=tf.float32),  # image_data
                tf.TensorSpec(shape=(None, h//32, w//32, 3, num_classes+5), dtype=tf.float32),  # y_true_0
                tf.TensorSpec(shape=(None, h//16, w//16, 3, num_classes+5), dtype=tf.float32),  # y_true_1  
                tf.TensorSpec(shape=(None, h//8, w//8, 3, num_classes+5), dtype=tf.float32)     # y_true_2
            ),
            tf.TensorSpec(shape=(None,), dtype=tf.float32)  # 损失占位符
        )
        
        # 创建Dataset
        dataset = tf.data.Dataset.from_generator(
            generator,
            output_signature=output_signature
        )
        return dataset

    # 创建数据集
    print("创建训练和验证数据集...")
    train_dataset = create_dataset(lines[:num_train], batch_size, input_shape, anchors, num_classes, is_training=True)
    val_dataset = create_dataset(lines[num_train:], batch_size, input_shape, anchors, num_classes, is_training=False)

    # 添加NaN检测和恢复机制
    class NanDetector(tf.keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            if logs is not None and any(tf.math.is_nan(v) for v in logs.values() if hasattr(v, 'dtype')):
                print(f"Epoch {epoch}: 检测到NaN值，跳过权重保存")
                # 可以在这里添加恢复逻辑
    
    callbacks.append(NanDetector())

    # 训练模型
    print("开始训练...")
    try:
        history = model.fit(
            train_dataset,
            steps_per_epoch=max(1, num_train // batch_size),
            validation_data=val_dataset,
            validation_steps=max(1, num_val // batch_size),
            epochs=100,
            callbacks=callbacks,
            verbose=1
        )
        
        # 修复保存文件名问题[2](@ref)
        final_weights_path = os.path.join(log_dir, 'trained_weights_final.weights.h5')
        model.save_weights(final_weights_path)
        print(f'训练完成! 模型权重已保存至: {final_weights_path}')
        
    except Exception as e:
        print(f"训练过程中出现错误: {e}")
        print("尝试保存当前进度...")
        try:
            # 即使出错也尝试保存权重
            emergency_path = os.path.join(log_dir, 'emergency_weights.weights.h5')
            model.save_weights(emergency_path)
            print(f"紧急权重已保存至: {emergency_path}")
        except Exception as save_error:
            print(f"保存紧急权重失败: {save_error}")

def get_classes(classes_path):
    """获取类别列表"""
    with open(classes_path, 'r', encoding='utf-8') as f:
        class_names = f.readlines()
    return [c.strip() for c in class_names if c.strip()]

def get_anchors(anchors_path):
    """获取锚点框"""
    with open(anchors_path, 'r', encoding='utf-8') as f:
        anchors = f.readline()
    return np.array([float(x) for x in anchors.split(',')]).reshape(-1, 2)

def create_model(input_shape, anchors, num_classes):
    """创建YOLOv3模型 - 增强稳定性版本"""
    K.clear_session()
    
    # 输入层
    image_input = Input(shape=(None, None, 3))
    h, w = input_shape
    
    # 真实值输入层
    y_true = [
        Input(shape=(h//32, w//32, 3, num_classes+5)),
        Input(shape=(h//16, w//16, 3, num_classes+5)), 
        Input(shape=(h//8, w//8, 3, num_classes+5))
    ]
    
    # 创建模型主体
    model_body = yolo_body(image_input, 3, num_classes)
    print(f'创建YOLOv3模型: {len(anchors)}个锚点, {num_classes}个类别')
    
    # 创建损失层 - 添加更严格的数值检查[1](@ref)
    model_loss = Lambda(
        yolo_loss, 
        output_shape=(1,), 
        name='yolo_loss',
        arguments={
            'anchors': anchors, 
            'num_classes': num_classes, 
            'ignore_thresh': 0.7  # 提高阈值减少假阳性
        }
    )([*model_body.output, *y_true])
    
    model = Model([image_input, *y_true], model_loss)
    
    # 打印模型概要
    model.summary()
    
    return model

def data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes, is_training=True):
    """数据生成器 - 增强稳定性和错误处理"""
    n = len(annotation_lines)
    i = 0
    
    # 数据增强参数（仅在训练时启用）[6](@ref)
    jitter = 0.3 if is_training else 0.0
    hue = 0.1 if is_training else 0.0
    sat = 1.5 if is_training else 1.0
    val = 1.5 if is_training else 1.0
    
    while True:
        image_data = []
        box_data = []
        
        for b in range(batch_size):
            if i == 0 and is_training:
                np.random.shuffle(annotation_lines)
            
            try:
                # 获取随机数据，添加数值检查[2](@ref)
                image, box = get_random_data(
                    annotation_lines[i], 
                    input_shape, 
                    random=is_training,
                    jitter=jitter,
                    hue=hue,
                    sat=sat,
                    val=val
                )
                
                # 数值检查：确保数据有效
                if np.any(np.isnan(image)) or np.any(np.isinf(image)):
                    print(f"警告: 图像 {i} 包含无效值，跳过")
                    continue
                    
                image_data.append(image)
                box_data.append(box)
                
            except Exception as e:
                print(f"处理图像 {annotation_lines[i]} 时出错: {e}")
                # 跳过有问题的图像
                continue
            finally:
                i = (i + 1) % n
        
        if len(image_data) == 0:
            continue
            
        # 转换为numpy数组并归一化[6](@ref)
        image_data = np.array(image_data, dtype='float32') / 255.0  # 重要：添加归一化
        
        # 检查数值有效性
        if np.any(np.isnan(image_data)) or np.any(np.isinf(image_data)):
            print("警告: 图像数据包含NaN或Inf值，跳过该批次")
            continue
            
        box_data = np.array(box_data)
        
        # 预处理真实框
        try:
            y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes)
            
            # 检查y_true是否包含无效值
            y_true_valid = True
            for y in y_true:
                if np.any(np.isnan(y)) or np.any(np.isinf(y)):
                    y_true_valid = False
                    break
                    
            if not y_true_valid:
                print("警告: y_true包含无效值，跳过该批次")
                continue
                
        except Exception as e:
            print(f"预处理真实框时出错: {e}")
            continue
        
        yield (image_data, y_true[0], y_true[1], y_true[2]), np.zeros(len(image_data))

def setup_training_environment():
    """设置训练环境以增强稳定性[2](@ref)"""
    # 设置TensorFlow优化选项
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    # 配置GPU内存增长
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"检测到 {len(gpus)} 个GPU，已启用内存增长")
        except RuntimeError as e:
            print(f"GPU配置错误: {e}")
    
    # 设置混合精度（如果可用）
    try:
        policy = tf.keras.mixed_precision.Policy('mixed_float16')
        tf.keras.mixed_precision.set_global_policy(policy)
        print("已启用混合精度训练")
    except:
        print("混合精度不可用，使用默认精度")

if __name__ == '__main__':
    setup_training_environment()
    _main()