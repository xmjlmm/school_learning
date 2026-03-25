# # """
# # Retrain the YOLO model for your own dataset.
# # """

# # import numpy as np
# # import keras.backend as K
# # from keras.layers import Input, Lambda
# # from keras.models import Model
# # from keras.optimizers import Adam
# # from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

# # from yolo3.model import preprocess_true_boxes, yolo_body, tiny_yolo_body, yolo_loss
# # from yolo3.utils import get_random_data


# # def _main():
# #     annotation_path = 'train.txt'
# #     log_dir = 'logs/000/'
# #     classes_path = 'model_data/voc_classes.txt'
# #     anchors_path = 'model_data/yolo_anchors.txt'
# #     class_names = get_classes(classes_path)
# #     num_classes = len(class_names)
# #     anchors = get_anchors(anchors_path)

# #     input_shape = (416,416) # multiple of 32, hw

# #     is_tiny_version = len(anchors)==6 # default setting
# #     if is_tiny_version:
# #         model = create_tiny_model(input_shape, anchors, num_classes,
# #             freeze_body=2, weights_path='model_data/tiny_yolo_weights.h5')
# #     else:
# #         model = create_model(input_shape, anchors, num_classes,
# #             freeze_body=2, weights_path='model_data/yolo_weights.h5') # make sure you know what you freeze

# #     logging = TensorBoard(log_dir=log_dir)
# #     checkpoint = ModelCheckpoint(log_dir + 'ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5',
# #         monitor='val_loss', save_weights_only=True, save_best_only=True, period=3)
# #     reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, verbose=1)
# #     early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1)

# #     val_split = 0.1
# #     with open(annotation_path) as f:
# #         lines = f.readlines()
# #     np.random.seed(10101)
# #     np.random.shuffle(lines)
# #     np.random.seed(None)
# #     num_val = int(len(lines)*val_split)
# #     num_train = len(lines) - num_val

# #     # Train with frozen layers first, to get a stable loss.
# #     # Adjust num epochs to your dataset. This step is enough to obtain a not bad model.
# #     if True:
# #         model.compile(optimizer=Adam(lr=1e-3), loss={
# #             # use custom yolo_loss Lambda layer.
# #             'yolo_loss': lambda y_true, y_pred: y_pred})

# #         batch_size = 32
# #         print('Train on {} samples, val on {} samples, with batch size {}.'.format(num_train, num_val, batch_size))
# #         model.fit_generator(data_generator_wrapper(lines[:num_train], batch_size, input_shape, anchors, num_classes),
# #                 steps_per_epoch=max(1, num_train//batch_size),
# #                 validation_data=data_generator_wrapper(lines[num_train:], batch_size, input_shape, anchors, num_classes),
# #                 validation_steps=max(1, num_val//batch_size),
# #                 epochs=50,
# #                 initial_epoch=0,
# #                 callbacks=[logging, checkpoint])
# #         model.save_weights(log_dir + 'trained_weights_stage_1.h5')

# #     # Unfreeze and continue training, to fine-tune.
# #     # Train longer if the result is not good.
# #     if True:
# #         for i in range(len(model.layers)):
# #             model.layers[i].trainable = True
# #         model.compile(optimizer=Adam(lr=1e-4), loss={'yolo_loss': lambda y_true, y_pred: y_pred}) # recompile to apply the change
# #         print('Unfreeze all of the layers.')

# #         batch_size = 32 # note that more GPU memory is required after unfreezing the body
# #         print('Train on {} samples, val on {} samples, with batch size {}.'.format(num_train, num_val, batch_size))
# #         model.fit_generator(data_generator_wrapper(lines[:num_train], batch_size, input_shape, anchors, num_classes),
# #             steps_per_epoch=max(1, num_train//batch_size),
# #             validation_data=data_generator_wrapper(lines[num_train:], batch_size, input_shape, anchors, num_classes),
# #             validation_steps=max(1, num_val//batch_size),
# #             epochs=100,
# #             initial_epoch=50,
# #             callbacks=[logging, checkpoint, reduce_lr, early_stopping])
# #         model.save_weights(log_dir + 'trained_weights_final.h5')

# #     # Further training if needed.


# # def get_classes(classes_path):
# #     '''loads the classes'''
# #     with open(classes_path) as f:
# #         class_names = f.readlines()
# #     class_names = [c.strip() for c in class_names]
# #     return class_names

# # def get_anchors(anchors_path):
# #     '''loads the anchors from a file'''
# #     with open(anchors_path) as f:
# #         anchors = f.readline()
# #     anchors = [float(x) for x in anchors.split(',')]
# #     return np.array(anchors).reshape(-1, 2)


# # def create_model(input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2,
# #             weights_path='model_data/yolo_weights.h5'):
# #     '''create the training model'''
# #     K.clear_session() # get a new session
# #     image_input = Input(shape=(None, None, 3))
# #     h, w = input_shape
# #     num_anchors = len(anchors)

# #     y_true = [Input(shape=(h//{0:32, 1:16, 2:8}[l], w//{0:32, 1:16, 2:8}[l], \
# #         num_anchors//3, num_classes+5)) for l in range(3)]

# #     model_body = yolo_body(image_input, num_anchors//3, num_classes)
# #     print('Create YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

# #     if load_pretrained:
# #         model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
# #         print('Load weights {}.'.format(weights_path))
# #         if freeze_body in [1, 2]:
# #             # Freeze darknet53 body or freeze all but 3 output layers.
# #             num = (185, len(model_body.layers)-3)[freeze_body-1]
# #             for i in range(num): model_body.layers[i].trainable = False
# #             print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

# #     model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
# #         arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.5})(
# #         [*model_body.output, *y_true])
# #     model = Model([model_body.input, *y_true], model_loss)

# #     return model

# # def create_tiny_model(input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2,
# #             weights_path='model_data/tiny_yolo_weights.h5'):
# #     '''create the training model, for Tiny YOLOv3'''
# #     K.clear_session() # get a new session
# #     image_input = Input(shape=(None, None, 3))
# #     h, w = input_shape
# #     num_anchors = len(anchors)

# #     y_true = [Input(shape=(h//{0:32, 1:16}[l], w//{0:32, 1:16}[l], \
# #         num_anchors//2, num_classes+5)) for l in range(2)]

# #     model_body = tiny_yolo_body(image_input, num_anchors//2, num_classes)
# #     print('Create Tiny YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

# #     if load_pretrained:
# #         model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
# #         print('Load weights {}.'.format(weights_path))
# #         if freeze_body in [1, 2]:
# #             # Freeze the darknet body or freeze all but 2 output layers.
# #             num = (20, len(model_body.layers)-2)[freeze_body-1]
# #             for i in range(num): model_body.layers[i].trainable = False
# #             print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

# #     model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
# #         arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.7})(
# #         [*model_body.output, *y_true])
# #     model = Model([model_body.input, *y_true], model_loss)

# #     return model

# # def data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes):
# #     '''data generator for fit_generator'''
# #     n = len(annotation_lines)
# #     i = 0
# #     while True:
# #         image_data = []
# #         box_data = []
# #         for b in range(batch_size):
# #             if i==0:
# #                 np.random.shuffle(annotation_lines)
# #             image, box = get_random_data(annotation_lines[i], input_shape, random=True)
# #             image_data.append(image)
# #             box_data.append(box)
# #             i = (i+1) % n
# #         image_data = np.array(image_data)
# #         box_data = np.array(box_data)
# #         y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes)
# #         yield [image_data, *y_true], np.zeros(batch_size)

# # def data_generator_wrapper(annotation_lines, batch_size, input_shape, anchors, num_classes):
# #     n = len(annotation_lines)
# #     if n==0 or batch_size<=0: return None
# #     return data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes)

# # if __name__ == '__main__':
# #     _main()


# """
# Retrain the YOLO model for your own dataset.
# """
# import os
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras import backend as K
# from tensorflow.keras.layers import Input, Lambda
# from tensorflow.keras.models import Model
# from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping

# from yolo3.model import preprocess_true_boxes, yolo_body, tiny_yolo_body, yolo_loss
# from yolo3.utils import get_random_data


# def _main():
#     # annotation_path = 'train.txt'
#     annotation_path = r'F:\data\VOC2007\ImageSets\Main\train.txt'

#     # log_dir = 'logs/000/'
#     log_dir = r'F:\data\VOC2007\logs\000'

#     # 确保日志目录存在
#     os.makedirs(log_dir, exist_ok=True)
    
#     # classes_path = 'model_data/voc_classes.txt'
#     # anchors_path = 'model_data/yolo_anchors.txt'
#     classes_path = r'F:\PycharmProjects\pythonProject\大四上\专项课程\keras-yolo3-master\model_data\voc_classes.txt'    
#     anchors_path = r'F:\PycharmProjects\pythonProject\大四上\专项课程\keras-yolo3-master\model_data\yolo_anchors.txt'
  
#     class_names = get_classes(classes_path)
#     anchors = get_anchors(anchors_path)
#     input_shape = (416, 416)  # multiple of 32, hw
    
#     # 创建模型
#     model = create_model(input_shape, anchors, len(class_names))
    
#     # 训练模型
#     train(model, annotation_path, input_shape, anchors, len(class_names), log_dir=log_dir)


# def train(model, annotation_path, input_shape, anchors, num_classes, log_dir='logs/'):
#     # 编译模型
#     model.compile(optimizer='adam', loss={
#         'yolo_loss': lambda y_true, y_pred: y_pred})
    
#     # 设置回调函数
#     logging = TensorBoard(log_dir=log_dir)
    
#     # 修改：使用正确的文件扩展名.weights.h5
#     checkpoint_filename = os.path.join(log_dir, "ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.weights.h5")
#     checkpoint = ModelCheckpoint(
#         checkpoint_filename,
#         monitor='val_loss', 
#         save_weights_only=True, 
#         save_best_only=True, 
#         save_freq='epoch'
#     )
    
#     batch_size = 10
#     val_split = 0.1
    
#     # 读取训练数据
#     with open(annotation_path, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
    
#     np.random.shuffle(lines)
#     num_val = int(len(lines) * val_split)
#     num_train = len(lines) - num_val
    
#     print('Train on {} samples, val on {} samples, with batch size {}.'.format(num_train, num_val, batch_size))
#     print(f"Logs will be saved to: {log_dir}")

#     # 关键修改：创建 tf.data.Dataset 并正确定义 output_signature
#     def create_dataset(annotation_lines, batch_size, input_shape, anchors, num_classes):
#         """创建符合 TensorFlow 2.x 要求的 Dataset"""
#         def generator():
#             return data_generator_wrap(annotation_lines, batch_size, input_shape, anchors, num_classes)
        
#         # 正确定义 output_signature
#         h, w = input_shape
#         num_anchors = len(anchors)
        
#         # 定义输入签名：image_data + 3个y_true输出
#         input_signature = (
#             tf.TensorSpec(shape=(None, h, w, 3), dtype=tf.float32),  # image_data
#             tf.TensorSpec(shape=(None, h//32, w//32, num_anchors//3, num_classes+5), dtype=tf.float32),  # y_true_0
#             tf.TensorSpec(shape=(None, h//16, w//16, num_anchors//3, num_classes+5), dtype=tf.float32),  # y_true_1
#             tf.TensorSpec(shape=(None, h//8, w//8, num_anchors//3, num_classes+5), dtype=tf.float32)   # y_true_2
#         )
#         output_signature = tf.TensorSpec(shape=(None,), dtype=tf.float32)  # dummy target
        
#         # 完整的签名格式
#         signature = (input_signature, output_signature)
        
#         # 创建 Dataset
#         dataset = tf.data.Dataset.from_generator(
#             generator,
#             output_signature=signature
#         )
#         return dataset

#     # 创建训练和验证数据集
#     train_dataset = create_dataset(lines[:num_train], batch_size, input_shape, anchors, num_classes)
#     val_dataset = create_dataset(lines[num_train:], batch_size, input_shape, anchors, num_classes)

#     # 使用修改后的 fit() 方法
#     model.fit(
#         train_dataset,
#         steps_per_epoch=max(1, num_train // batch_size),
#         validation_data=val_dataset,
#         validation_steps=max(1, num_val // batch_size),
#         epochs=5,
#         initial_epoch=0,
#         callbacks=[logging, checkpoint]
#     )
    
#     # 保存最终权重
#     final_weights_path = os.path.join(log_dir, 'trained_weights.weights.h5')
#     model.save_weights(final_weights_path)
#     print(f"Training completed! Final weights saved to: {final_weights_path}")


# def get_classes(classes_path):
#     with open(classes_path, 'r', encoding='utf-8') as f:
#         class_names = f.readlines()
#     class_names = [c.strip() for c in class_names]
#     return class_names


# def get_anchors(anchors_path):
#     with open(anchors_path, 'r', encoding='utf-8') as f:
#         anchors = f.readline()
#     anchors = [float(x) for x in anchors.split(',')]
#     return np.array(anchors).reshape(-1, 2)


# def create_model(input_shape, anchors, num_classes, load_pretrained=False, freeze_body=False,
#                  weights_path='model_data/yolo_weights.h5'):
#     K.clear_session()  # get a new session
#     image_input = Input(shape=(None, None, 3))
#     h, w = input_shape
#     num_anchors = len(anchors)
    
#     y_true = [Input(shape=(h//{0:32, 1:16, 2:8}[l], w//{0:32, 1:16, 2:8}[l], 
#                num_anchors//3, num_classes+5)) for l in range(3)]

#     model_body = yolo_body(image_input, num_anchors//3, num_classes)
#     print('Create YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

#     if load_pretrained:
#         model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
#         print('Load weights {}.'.format(weights_path))
#         if freeze_body:
#             # Do not freeze 3 output layers.
#             num = len(model_body.layers) - 7
#             for i in range(num): 
#                 model_body.layers[i].trainable = False
#             print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

#     model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
#         arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.5})(
#         [*model_body.output, *y_true])
#     model = Model([model_body.input, *y_true], model_loss)
#     return model


# def data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes):
#     n = len(annotation_lines)
#     np.random.shuffle(annotation_lines)
#     i = 0
#     while True:
#         image_data = []
#         box_data = []
#         for b in range(batch_size):
#             i %= n
#             image, box = get_random_data(annotation_lines[i], input_shape, random=True)
#             image_data.append(image)
#             box_data.append(box)
#             i += 1
#         image_data = np.array(image_data)
#         box_data = np.array(box_data)
#         y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes)
#         yield [image_data, *y_true], np.zeros(batch_size)


# def data_generator_wrap(annotation_lines, batch_size, input_shape, anchors, num_classes):
#     n = len(annotation_lines)
#     if n == 0 or batch_size <= 0: 
#         return None
#     return data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes)


# if __name__ == '__main__':
#     _main()






"""
修复版的YOLOv3训练脚本 - 解决output_signature类型错误
"""
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
    """主训练函数"""
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
    """修复output_signature问题的训练函数"""
    
    # 编译模型
    model.compile(optimizer=Adam(learning_rate=1e-3), 
                  loss={'yolo_loss': lambda y_true, y_pred: y_pred})
    
    # 回调函数
    callbacks = [
        TensorBoard(log_dir=log_dir),
        ModelCheckpoint(os.path.join(log_dir, "ep{epoch:03d}-loss{loss:.3f}.weights.h5"),
                       save_weights_only=True, save_best_only=True),
        ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, verbose=1),
        EarlyStopping(monitor='loss', patience=15, verbose=1)
    ]
    
    batch_size = 16
    val_split = 0.1
    
    # 读取数据
    with open(annotation_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    np.random.shuffle(lines)
    num_val = int(len(lines) * val_split)
    num_train = len(lines) - num_val
    
    print(f'训练样本: {num_train}, 验证样本: {num_val}, 批量大小: {batch_size}')

    # 关键修复：正确的output_signature定义
    def create_dataset(annotation_lines, batch_size, input_shape, anchors, num_classes):
        """创建符合TensorFlow要求的Dataset"""
        def generator():
            return data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes)
        
        # 正确的output_signature定义 - 使用元组而不是列表
        h, w = input_shape
        
        # 输入签名：必须是元组结构
        input_signature = (
            tf.TensorSpec(shape=(None, h, w, 3), dtype=tf.float32),  # image_data
            tf.TensorSpec(shape=(None, h//32, w//32, 3, num_classes+5), dtype=tf.float32),  # y_true_0
            tf.TensorSpec(shape=(None, h//16, w//16, 3, num_classes+5), dtype=tf.float32),  # y_true_1  
            tf.TensorSpec(shape=(None, h//8, w//8, 3, num_classes+5), dtype=tf.float32)     # y_true_2
        )
        
        # 输出签名
        output_signature = tf.TensorSpec(shape=(None,), dtype=tf.float32)
        
        # 完整的签名格式：必须是元组(input_signature, output_signature)
        signature = (input_signature, output_signature)
        
        # 创建Dataset
        dataset = tf.data.Dataset.from_generator(
            generator,
            output_signature=signature
        )
        return dataset

    # 创建数据集
    train_dataset = create_dataset(lines[:num_train], batch_size, input_shape, anchors, num_classes)
    val_dataset = create_dataset(lines[num_train:], batch_size, input_shape, anchors, num_classes)

    # 训练模型
    model.fit(
        train_dataset,
        steps_per_epoch=max(1, num_train // batch_size),
        validation_data=val_dataset,
        validation_steps=max(1, num_val // batch_size),
        epochs=100,
        callbacks=callbacks,
        verbose=1
    )
    
    model.save_weights(os.path.join(log_dir, 'trained_weights_final.h5'))
    print('训练完成!')

def get_classes(classes_path):
    with open(classes_path) as f:
        class_names = f.readlines()
    return [c.strip() for c in class_names]

def get_anchors(anchors_path):
    with open(anchors_path) as f:
        anchors = f.readline()
    return np.array([float(x) for x in anchors.split(',')]).reshape(-1, 2)

def create_model(input_shape, anchors, num_classes):
    """创建YOLOv3模型"""
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
    
    # 创建损失层
    model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
                       arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.5})(
        [*model_body.output, *y_true])
    
    model = Model([image_input, *y_true], model_loss)
    return model

def data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes):
    """数据生成器 - 确保返回正确的数据结构"""
    n = len(annotation_lines)
    i = 0
    
    while True:
        image_data = []
        box_data = []
        
        for b in range(batch_size):
            if i == 0:
                np.random.shuffle(annotation_lines)
            
            # 获取随机数据
            image, box = get_random_data(annotation_lines[i], input_shape, random=True)
            image_data.append(image)
            box_data.append(box)
            i = (i + 1) % n
        
        # 转换为numpy数组
        image_data = np.array(image_data, dtype='float32')
        box_data = np.array(box_data)
        
        # 预处理真实框
        y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes)
        
        yield (image_data, y_true[0], y_true[1], y_true[2]), np.zeros(batch_size)

if __name__ == '__main__':
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    _main()


