"""
增强版YOLOv3训练脚本 - 完整TensorBoard集成与优化
修复output_signature类型错误，集成可视化监控
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Input, Lambda
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

from yolo3.model import preprocess_true_boxes, yolo_body, yolo_loss
from yolo3.utils import get_random_data

class EnhancedTensorBoard(TensorBoard):
    """增强的TensorBoard回调类，支持更多监控指标"""
    
    def __init__(self, log_dir, **kwargs):
        # 添加时间戳确保每次训练有独立目录
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_dir = os.path.join(log_dir, timestamp)
        super(EnhancedTensorBoard, self).__init__(
            log_dir=self.log_dir,
            histogram_freq=1,           # 每个epoch记录直方图
            write_graph=True,           # 记录计算图
            write_images=False,         # 不记录权重图像（节省空间）
            update_freq='epoch',       # 每个epoch更新
            profile_batch=0,            # 禁用性能分析
            **kwargs
        )
        
    def on_epoch_end(self, epoch, logs=None):
        """在每个epoch结束时记录额外指标"""
        logs = logs or {}
        
        # 记录当前学习率
        try:
            lr = float(K.get_value(self.model.optimizer.lr))
            logs['learning_rate'] = lr
        except:
            pass
            
        super(EnhancedTensorBoard, self).on_epoch_end(epoch, logs)

def _main():
    """主训练函数 - 增强错误处理和路径验证"""
    try:
        # 配置文件路径
        annotation_path = 'F:/data/VOC2007/ImageSets/Main/2007_train.txt'
        log_dir = 'F:/data/VOC2007/logs/000'
        classes_path = 'F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/voc_classes.txt'
        anchors_path = 'F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/yolo_anchors.txt'
        
        # 验证文件存在性
        for path in [annotation_path, classes_path, anchors_path]:
            if not os.path.exists(path):
                raise FileNotFoundError(f"文件不存在: {path}")
        
        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)
        
        # 获取配置信息
        class_names = get_classes(classes_path)
        anchors = get_anchors(anchors_path)
        input_shape = (416, 416)
        
        print("=" * 70)
        print("YOLOv3模型训练启动")
        print("=" * 70)
        print(f"📊 数据集信息:")
        print(f"   - 类别数量: {len(class_names)}")
        print(f"   - 锚点数量: {len(anchors)}")
        print(f"   - 输入尺寸: {input_shape}")
        print(f"   - 日志目录: {log_dir}")
        print("=" * 70)
        
        # 创建模型
        model = create_model(input_shape, anchors, len(class_names))
        
        # 开始训练
        train(model, annotation_path, input_shape, anchors, len(class_names), log_dir=log_dir)
        
    except Exception as e:
        print(f"❌ 初始化错误: {e}")
        import traceback
        traceback.print_exc()

def train(model, annotation_path, input_shape, anchors, num_classes, log_dir='logs/'):
    """增强的训练函数 - 集成完整TensorBoard监控"""
    
    # 编译模型
    model.compile(
        optimizer=Adam(learning_rate=1e-3), 
        loss={'yolo_loss': lambda y_true, y_pred: y_pred}
    )
    
    # 创建增强的TensorBoard回调
    tensorboard_callback = EnhancedTensorBoard(log_dir=log_dir)
    
    # 完整的回调函数列表
    callbacks = [
        tensorboard_callback,  # TensorBoard可视化
        
        # 模型检查点配置
        ModelCheckpoint(
            os.path.join(tensorboard_callback.log_dir, "best_model.weights.h5"),
            monitor='val_loss',
            save_weights_only=True,
            save_best_only=True,
            verbose=1
        ),
        
        # 周期保存检查点
        ModelCheckpoint(
            os.path.join(tensorboard_callback.log_dir, "epoch_{epoch:03d}_loss_{loss:.3f}.weights.h5"),
            save_weights_only=True,
            save_freq='epoch',
            verbose=0
        ),
        
        # 学习率动态调整
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-6,
            verbose=1
        ),
        
        # 早停机制
        EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True,
            verbose=1
        )
    ]
    
    # 训练参数配置
    batch_size = 16
    val_split = 0.1
    epochs = 100
    
    # 读取和预处理数据
    try:
        with open(annotation_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if len(lines) == 0:
            raise ValueError("训练数据文件为空")
            
    except Exception as e:
        print(f"❌ 数据加载错误: {e}")
        return None
    
    # 数据划分
    np.random.shuffle(lines)
    num_val = int(len(lines) * val_split)
    num_train = len(lines) - num_val
    
    # 设置TensorBoard的训练样本信息
    tensorboard_callback.train_samples = num_train
    tensorboard_callback.val_samples = num_val
    
    print(f"📈 训练配置:")
    print(f"   - 训练样本: {num_train}")
    print(f"   - 验证样本: {num_val}") 
    print(f"   - 批量大小: {batch_size}")
    print(f"   - 训练轮数: {epochs}")
    
    # 关键修复：正确的output_signature定义
    def create_tf_dataset(annotation_lines, batch_size, input_shape, anchors, num_classes):
        """创建符合TensorFlow 2.x要求的Dataset"""
        
        def data_generator():
            """数据生成器内部函数"""
            n = len(annotation_lines)
            i = 0
            
            while True:
                image_data = []
                box_data = []
                
                for b in range(batch_size):
                    if i == 0:
                        np.random.shuffle(annotation_lines)
                    
                    image, box = get_random_data(annotation_lines[i], input_shape, random=True)
                    image_data.append(image)
                    box_data.append(box)
                    i = (i + 1) % n
                
                image_data = np.array(image_data, dtype='float32')
                box_data = np.array(box_data)
                
                y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes)
                
                # 返回正确的数据格式
                yield (image_data, y_true[0], y_true[1], y_true[2]), np.zeros(batch_size)
        
        # 定义正确的output_signature
        h, w = input_shape
        
        # 输入特征签名
        input_signature = (
            tf.TensorSpec(shape=(None, h, w, 3), dtype=tf.float32),  # image_data
            tf.TensorSpec(shape=(None, h//32, w//32, 3, num_classes+5), dtype=tf.float32),  # y_true_0
            tf.TensorSpec(shape=(None, h//16, w//16, 3, num_classes+5), dtype=tf.float32),   # y_true_1
            tf.TensorSpec(shape=(None, h//8, w//8, 3, num_classes+5), dtype=tf.float32)     # y_true_2
        )
        
        # 输出标签签名
        output_signature = tf.TensorSpec(shape=(None,), dtype=tf.float32)
        
        # 创建Dataset
        dataset = tf.data.Dataset.from_generator(
            data_generator,
            output_signature=(input_signature, output_signature)
        )
        
        return dataset
    
    # 创建训练和验证数据集
    try:
        train_dataset = create_tf_dataset(lines[:num_train], batch_size, input_shape, anchors, num_classes)
        val_dataset = create_tf_dataset(lines[num_train:], batch_size, input_shape, anchors, num_classes)
        
    except Exception as e:
        print(f"❌ 数据集创建错误: {e}")
        # 回退到简单生成器模式
        return train_simple_mode(model, lines, batch_size, input_shape, anchors, num_classes, 
                               num_train, num_val, callbacks, epochs, tensorboard_callback.log_dir)
    
    # 计算训练步数
    train_steps = max(1, num_train // batch_size)
    val_steps = max(1, num_val // batch_size)
    
    print(f"👣 训练参数:")
    print(f"   - 每个epoch训练步数: {train_steps}")
    print(f"   - 每个epoch验证步数: {val_steps}")
    print(f"   - TensorBoard目录: {tensorboard_callback.log_dir}")
    
    print("🚀 开始训练过程...")
    
    try:
        # 训练模型
        history = model.fit(
            train_dataset,
            steps_per_epoch=train_steps,
            validation_data=val_dataset,
            validation_steps=val_steps,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        # 保存最终模型
        final_path = os.path.join(tensorboard_callback.log_dir, 'trained_weights_final.weights.h5')
        model.save_weights(final_path)
        
        print("✅ 训练完成!")
        print(f"💾 模型权重保存至: {final_path}")
        print(f"📊 使用以下命令启动TensorBoard:")
        print(f"   tensorboard --logdir=\"{tensorboard_callback.log_dir}\"")
        print(f"🌐 然后在浏览器中访问: http://localhost:6006")
        
        return history
        
    except Exception as e:
        print(f"❌ 训练过程错误: {e}")
        import traceback
        traceback.print_exc()
        return None

def train_simple_mode(model, lines, batch_size, input_shape, anchors, num_classes, 
                     num_train, num_val, callbacks, epochs, log_dir):
    """简单训练模式 - 兼容性回退方案"""
    print("⚠️  使用兼容性训练模式...")
    
    def simple_generator(annotation_lines, batch_size, input_shape, anchors, num_classes):
        """简化数据生成器"""
        n = len(annotation_lines)
        i = 0
        
        while True:
            image_data = []
            box_data = []
            
            for b in range(batch_size):
                if i == 0:
                    np.random.shuffle(annotation_lines)
                
                image, box = get_random_data(annotation_lines[i], input_shape, random=True)
                image_data.append(image)
                box_data.append(box)
                i = (i + 1) % n
            
            image_data = np.array(image_data, dtype='float32')
            box_data = np.array(box_data)
            
            y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes)
            
            yield [image_data, *y_true], np.zeros(batch_size)
    
    # 计算步数
    train_steps = max(1, num_train // batch_size)
    val_steps = max(1, num_val // batch_size)
    
    # 训练模型
    history = model.fit(
        simple_generator(lines[:num_train], batch_size, input_shape, anchors, num_classes),
        steps_per_epoch=train_steps,
        validation_data=simple_generator(lines[num_train:], batch_size, input_shape, anchors, num_classes),
        validation_steps=val_steps,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )
    
    # 保存模型
    final_path = os.path.join(log_dir, 'trained_weights_final.weights.h5')
    model.save_weights(final_path)
    
    print("✅ 兼容性训练完成!")
    return history

def get_classes(classes_path):
    """安全读取类别文件"""
    try:
        with open(classes_path, 'r', encoding='utf-8') as f:
            class_names = f.readlines()
        return [c.strip() for c in class_names if c.strip()]
    except Exception as e:
        print(f"⚠️  读取类别文件错误，使用默认类别: {e}")
        return ['object']

def get_anchors(anchors_path):
    """安全读取锚点文件"""
    try:
        with open(anchors_path, 'r', encoding='utf-8') as f:
            anchors = f.readline()
        return np.array([float(x) for x in anchors.split(',')]).reshape(-1, 2)
    except Exception as e:
        print(f"⚠️  读取锚点文件错误，使用默认锚点: {e}")
        return np.array([[10,13], [16,30], [33,23], [30,61], [62,45], 
                        [59,119], [116,90], [156,198], [373,326]])

def create_model(input_shape, anchors, num_classes, load_pretrained=False, weights_path=None):
    """创建YOLOv3模型"""
    K.clear_session()
    
    # 输入层
    image_input = Input(shape=(None, None, 3))
    h, w = input_shape
    
    # 真实值输入层
    y_true = [
        Input(shape=(h//32, w//32, 3, num_classes+5), name='y_true_0'),
        Input(shape=(h//16, w//16, 3, num_classes+5), name='y_true_1'), 
        Input(shape=(h//8, w//8, 3, num_classes+5), name='y_true_2')
    ]
    
    # 创建模型主体
    model_body = yolo_body(image_input, 3, num_classes)
    print(f"🔧 YOLOv3模型创建成功")
    print(f"   - 锚点数量: {len(anchors)}")
    print(f"   - 类别数量: {num_classes}")
    
    # 可选：加载预训练权重
    if load_pretrained and weights_path and os.path.exists(weights_path):
        try:
            model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
            print(f"🔗 预训练权重加载成功: {weights_path}")
        except Exception as e:
            print(f"⚠️  预训练权重加载失败: {e}")
    
    # 创建损失层
    model_loss = Lambda(
        yolo_loss, 
        output_shape=(1,), 
        name='yolo_loss',
        arguments={
            'anchors': anchors, 
            'num_classes': num_classes, 
            'ignore_thresh': 0.5
        }
    )([*model_body.output, *y_true])
    
    # 构建完整模型
    model = Model([image_input, *y_true], model_loss)
    
    # 打印模型信息
    total_params = model_body.count_params()
    print(f"📊 模型参数统计:")
    print(f"   - 总参数: {total_params:,}")
    print(f"   - 模型大小: {total_params * 4 / (1024**2):.2f} MB")
    
    return model

def setup_environment():
    """环境配置优化"""
    # 设置TensorFlow环境
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    
    # GPU配置
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"🎮 GPU配置完成: {len(gpus)}个GPU可用")
        except RuntimeError as e:
            print(f"⚠️  GPU配置警告: {e}")
    else:
        print("ℹ️  使用CPU进行训练")
    
    print(f"🔧 环境信息:")
    print(f"   - TensorFlow版本: {tf.__version__}")
    print(f"   - 工作目录: {os.getcwd()}")

if __name__ == '__main__':
    # 环境配置
    setup_environment()
    
    # 启动训练
    print("🎯 启动增强版YOLOv3训练流程")
    _main()