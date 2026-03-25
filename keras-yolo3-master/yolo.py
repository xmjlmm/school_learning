# # -*- coding: utf-8 -*-
# """
# Class definition of YOLO_v3 style detection model on image and video
# """

# import colorsys
# import os
# from timeit import default_timer as timer

# import numpy as np
# from keras import backend as K
# from keras.models import load_model
# from keras.layers import Input
# from PIL import Image, ImageFont, ImageDraw

# from yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
# from yolo3.utils import letterbox_image
# import os
# from keras.utils import multi_gpu_model

# class YOLO(object):
#     _defaults = {
#         # "model_path": 'model_data/yolo.h5',
#         "model_path": "F:/data/darknet53.conv.74",
#         "anchors_path": 'F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/yolo_anchors.txt',
#         "classes_path": 'F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/coco_classes.txt',
#         "score" : 0.3,
#         "iou" : 0.45,
#         "model_image_size" : (416, 416),
#         "gpu_num" : 1,
#     }

#     @classmethod
#     def get_defaults(cls, n):
#         if n in cls._defaults:
#             return cls._defaults[n]
#         else:
#             return "Unrecognized attribute name '" + n + "'"

#     def __init__(self, **kwargs):
#         self.__dict__.update(self._defaults) # set up default values
#         self.__dict__.update(kwargs) # and update with user overrides
#         self.class_names = self._get_class()
#         self.anchors = self._get_anchors()
#         self.sess = K.get_session()
#         self.boxes, self.scores, self.classes = self.generate()

#     def _get_class(self):
#         classes_path = os.path.expanduser(self.classes_path)
#         with open(classes_path) as f:
#             class_names = f.readlines()
#         class_names = [c.strip() for c in class_names]
#         return class_names

#     def _get_anchors(self):
#         anchors_path = os.path.expanduser(self.anchors_path)
#         with open(anchors_path) as f:
#             anchors = f.readline()
#         anchors = [float(x) for x in anchors.split(',')]
#         return np.array(anchors).reshape(-1, 2)

#     def generate(self):
#         model_path = os.path.expanduser(self.model_path)
#         assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

#         # Load model, or construct model and load weights.
#         num_anchors = len(self.anchors)
#         num_classes = len(self.class_names)
#         is_tiny_version = num_anchors==6 # default setting
#         try:
#             self.yolo_model = load_model(model_path, compile=False)
#         except:
#             self.yolo_model = tiny_yolo_body(Input(shape=(None,None,3)), num_anchors//2, num_classes) \
#                 if is_tiny_version else yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
#             self.yolo_model.load_weights(self.model_path) # make sure model, anchors and classes match
#         else:
#             assert self.yolo_model.layers[-1].output_shape[-1] == \
#                 num_anchors/len(self.yolo_model.output) * (num_classes + 5), \
#                 'Mismatch between model and given anchor and class sizes'

#         print('{} model, anchors, and classes loaded.'.format(model_path))

#         # Generate colors for drawing bounding boxes.
#         hsv_tuples = [(x / len(self.class_names), 1., 1.)
#                       for x in range(len(self.class_names))]
#         self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
#         self.colors = list(
#             map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
#                 self.colors))
#         np.random.seed(10101)  # Fixed seed for consistent colors across runs.
#         np.random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.
#         np.random.seed(None)  # Reset seed to default.

#         # Generate output tensor targets for filtered bounding boxes.
#         self.input_image_shape = K.placeholder(shape=(2, ))
#         if self.gpu_num>=2:
#             self.yolo_model = multi_gpu_model(self.yolo_model, gpus=self.gpu_num)
#         boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
#                 len(self.class_names), self.input_image_shape,
#                 score_threshold=self.score, iou_threshold=self.iou)
#         return boxes, scores, classes

#     def detect_image(self, image):
#         start = timer()

#         if self.model_image_size != (None, None):
#             assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
#             assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
#             boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
#         else:
#             new_image_size = (image.width - (image.width % 32),
#                               image.height - (image.height % 32))
#             boxed_image = letterbox_image(image, new_image_size)
#         image_data = np.array(boxed_image, dtype='float32')

#         print(image_data.shape)
#         image_data /= 255.
#         image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

#         out_boxes, out_scores, out_classes = self.sess.run(
#             [self.boxes, self.scores, self.classes],
#             feed_dict={
#                 self.yolo_model.input: image_data,
#                 self.input_image_shape: [image.size[1], image.size[0]],
#                 K.learning_phase(): 0
#             })

#         print('Found {} boxes for {}'.format(len(out_boxes), 'img'))

#         font = ImageFont.truetype(font='font/FiraMono-Medium.otf',
#                     size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
#         thickness = (image.size[0] + image.size[1]) // 300

#         for i, c in reversed(list(enumerate(out_classes))):
#             predicted_class = self.class_names[c]
#             box = out_boxes[i]
#             score = out_scores[i]

#             label = '{} {:.2f}'.format(predicted_class, score)
#             draw = ImageDraw.Draw(image)
#             label_size = draw.textsize(label, font)

#             top, left, bottom, right = box
#             top = max(0, np.floor(top + 0.5).astype('int32'))
#             left = max(0, np.floor(left + 0.5).astype('int32'))
#             bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
#             right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
#             print(label, (left, top), (right, bottom))

#             if top - label_size[1] >= 0:
#                 text_origin = np.array([left, top - label_size[1]])
#             else:
#                 text_origin = np.array([left, top + 1])

#             # My kingdom for a good redistributable image drawing library.
#             for i in range(thickness):
#                 draw.rectangle(
#                     [left + i, top + i, right - i, bottom - i],
#                     outline=self.colors[c])
#             draw.rectangle(
#                 [tuple(text_origin), tuple(text_origin + label_size)],
#                 fill=self.colors[c])
#             draw.text(text_origin, label, fill=(0, 0, 0), font=font)
#             del draw

#         end = timer()
#         print(end - start)
#         return image

#     def close_session(self):
#         self.sess.close()

# def detect_video(yolo, video_path, output_path=""):
#     import cv2
#     vid = cv2.VideoCapture(video_path)
#     if not vid.isOpened():
#         raise IOError("Couldn't open webcam or video")
#     video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
#     video_fps       = vid.get(cv2.CAP_PROP_FPS)
#     video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
#                         int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#     isOutput = True if output_path != "" else False
#     if isOutput:
#         print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
#         out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
#     accum_time = 0
#     curr_fps = 0
#     fps = "FPS: ??"
#     prev_time = timer()
#     while True:
#         return_value, frame = vid.read()
#         image = Image.fromarray(frame)
#         image = yolo.detect_image(image)
#         result = np.asarray(image)
#         curr_time = timer()
#         exec_time = curr_time - prev_time
#         prev_time = curr_time
#         accum_time = accum_time + exec_time
#         curr_fps = curr_fps + 1
#         if accum_time > 1:
#             accum_time = accum_time - 1
#             fps = "FPS: " + str(curr_fps)
#             curr_fps = 0
#         cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                     fontScale=0.50, color=(255, 0, 0), thickness=2)
#         cv2.namedWindow("result", cv2.WINDOW_NORMAL)
#         cv2.imshow("result", result)
#         if isOutput:
#             out.write(result)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     yolo.close_session()









# # -*- coding: utf-8 -*-
# """
# Class definition of YOLO_v3 style detection model on image and video
# """

# import colorsys
# import os
# from timeit import default_timer as timer

# import numpy as np
# from keras import backend as K
# from keras.models import load_model
# from keras.layers import Input
# from PIL import Image, ImageFont, ImageDraw

# from yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
# from yolo3.utils import letterbox_image
# import os
# from keras.utils import multi_gpu_model

# class YOLO(object):
#     _defaults = {
        
#         # "model_path": 'model_data/yolo.h5',
#         "model_path": "F:/data/VOC2007/logs/000/ep018-loss63.362.weights.h5",
#         "anchors_path": 'F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/yolo_anchors.txt',
#         "classes_path": 'F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/coco_classes.txt',
#         "score" : 0.3,
#         "iou" : 0.45,
#         "model_image_size" : (416, 416),
#         "gpu_num" : 1,
#     }

#     @classmethod
#     def get_defaults(cls, n):
#         if n in cls._defaults:
#             return cls._defaults[n]
#         else:
#             return "Unrecognized attribute name '" + n + "'"

#     def __init__(self, **kwargs):
#         self.__dict__.update(self._defaults) # set up default values
#         self.__dict__.update(kwargs) # and update with user overrides
#         self.class_names = self._get_class()
#         self.anchors = self._get_anchors()
#         self.sess = K.get_session()
#         self.boxes, self.scores, self.classes = self.generate()

#     def _get_class(self):
#         classes_path = os.path.expanduser(self.classes_path)
#         with open(classes_path) as f:
#             class_names = f.readlines()
#         class_names = [c.strip() for c in class_names]
#         return class_names

#     def _get_anchors(self):
#         anchors_path = os.path.expanduser(self.anchors_path)
#         with open(anchors_path) as f:
#             anchors = f.readline()
#         anchors = [float(x) for x in anchors.split(',')]
#         return np.array(anchors).reshape(-1, 2)

#     def generate(self):
#         model_path = os.path.expanduser(self.model_path)
#         assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

#         # Load model, or construct model and load weights.
#         num_anchors = len(self.anchors)
#         num_classes = len(self.class_names)
#         is_tiny_version = num_anchors==6 # default setting
#         try:
#             self.yolo_model = load_model(model_path, compile=False)
#         except:
#             self.yolo_model = tiny_yolo_body(Input(shape=(None,None,3)), num_anchors//2, num_classes) \
#                 if is_tiny_version else yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
#             self.yolo_model.load_weights(self.model_path) # make sure model, anchors and classes match
#         else:
#             assert self.yolo_model.layers[-1].output_shape[-1] == \
#                 num_anchors/len(self.yolo_model.output) * (num_classes + 5), \
#                 'Mismatch between model and given anchor and class sizes'

#         print('{} model, anchors, and classes loaded.'.format(model_path))

#         # Generate colors for drawing bounding boxes.
#         hsv_tuples = [(x / len(self.class_names), 1., 1.)
#                       for x in range(len(self.class_names))]
#         self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
#         self.colors = list(
#             map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
#                 self.colors))
#         np.random.seed(10101)  # Fixed seed for consistent colors across runs.
#         np.random.shuffle(self.colors)  # Shuffle colors to decorrelate adjacent classes.
#         np.random.seed(None)  # Reset seed to default.

#         # Generate output tensor targets for filtered bounding boxes.
#         self.input_image_shape = K.placeholder(shape=(2, ))
#         if self.gpu_num>=2:
#             self.yolo_model = multi_gpu_model(self.yolo_model, gpus=self.gpu_num)
#         boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
#                 len(self.class_names), self.input_image_shape,
#                 score_threshold=self.score, iou_threshold=self.iou)
#         return boxes, scores, classes

#     def detect_image(self, image):
#         start = timer()

#         if self.model_image_size != (None, None):
#             assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
#             assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
#             boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
#         else:
#             new_image_size = (image.width - (image.width % 32),
#                               image.height - (image.height % 32))
#             boxed_image = letterbox_image(image, new_image_size)
#         image_data = np.array(boxed_image, dtype='float32')

#         print(image_data.shape)
#         image_data /= 255.
#         image_data = np.expand_dims(image_data, 0)  # Add batch dimension.

#         out_boxes, out_scores, out_classes = self.sess.run(
#             [self.boxes, self.scores, self.classes],
#             feed_dict={
#                 self.yolo_model.input: image_data,
#                 self.input_image_shape: [image.size[1], image.size[0]],
#                 K.learning_phase(): 0
#             })

#         print('Found {} boxes for {}'.format(len(out_boxes), 'img'))

#         font = ImageFont.truetype(font='font/FiraMono-Medium.otf',
#                     size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
#         thickness = (image.size[0] + image.size[1]) // 300

#         for i, c in reversed(list(enumerate(out_classes))):
#             predicted_class = self.class_names[c]
#             box = out_boxes[i]
#             score = out_scores[i]

#             label = '{} {:.2f}'.format(predicted_class, score)
#             draw = ImageDraw.Draw(image)
#             label_size = draw.textsize(label, font)

#             top, left, bottom, right = box
#             top = max(0, np.floor(top + 0.5).astype('int32'))
#             left = max(0, np.floor(left + 0.5).astype('int32'))
#             bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
#             right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
#             print(label, (left, top), (right, bottom))

#             if top - label_size[1] >= 0:
#                 text_origin = np.array([left, top - label_size[1]])
#             else:
#                 text_origin = np.array([left, top + 1])

#             # My kingdom for a good redistributable image drawing library.
#             for i in range(thickness):
#                 draw.rectangle(
#                     [left + i, top + i, right - i, bottom - i],
#                     outline=self.colors[c])
#             draw.rectangle(
#                 [tuple(text_origin), tuple(text_origin + label_size)],
#                 fill=self.colors[c])
#             draw.text(text_origin, label, fill=(0, 0, 0), font=font)
#             del draw

#         end = timer()
#         print(end - start)
#         return image

#     def close_session(self):
#         self.sess.close()

# def detect_video(yolo, video_path, output_path=""):
#     import cv2
#     vid = cv2.VideoCapture(video_path)
#     if not vid.isOpened():
#         raise IOError("Couldn't open webcam or video")
#     video_FourCC    = int(vid.get(cv2.CAP_PROP_FOURCC))
#     video_fps       = vid.get(cv2.CAP_PROP_FPS)
#     video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
#                         int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#     isOutput = True if output_path != "" else False
#     if isOutput:
#         print("!!! TYPE:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
#         out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
#     accum_time = 0
#     curr_fps = 0
#     fps = "FPS: ??"
#     prev_time = timer()
#     while True:
#         return_value, frame = vid.read()
#         image = Image.fromarray(frame)
#         image = yolo.detect_image(image)
#         result = np.asarray(image)
#         curr_time = timer()
#         exec_time = curr_time - prev_time
#         prev_time = curr_time
#         accum_time = accum_time + exec_time
#         curr_fps = curr_fps + 1
#         if accum_time > 1:
#             accum_time = accum_time - 1
#             fps = "FPS: " + str(curr_fps)
#             curr_fps = 0
#         cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                     fontScale=0.50, color=(255, 0, 0), thickness=2)
#         cv2.namedWindow("result", cv2.WINDOW_NORMAL)
#         cv2.imshow("result", result)
#         if isOutput:
#             out.write(result)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     yolo.close_session()




# import colorsys
# import os
# from timeit import default_timer as timer

# import numpy as np
# import tensorflow as tf
# # 关键修复：使用 TensorFlow 2.x 标准的导入方式
# from tensorflow.keras import backend as K
# from tensorflow.keras.models import load_model
# from tensorflow.keras.layers import Input, Lambda
# from PIL import Image, ImageFont, ImageDraw

# from yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
# from yolo3.utils import letterbox_image
# import os

# # 移除兼容模式代码，使用 TensorFlow 2.x 原生方式
# # tf.compat.v1.disable_v2_behavior()  # 注释掉或删除这行

# class YOLO(object):
#     _defaults = {
#         "model_path": "F:/data/VOC2007/logs/000/ep018-loss63.362.weights.h5",
#         "anchors_path": 'F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/yolo_anchors.txt',
#         "classes_path": 'F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/coco_classes.txt',
#         "score": 0.3,
#         "iou": 0.45,
#         "model_image_size": (416, 416),
#         "gpu_num": 1,
#     }

#     @classmethod
#     def get_defaults(cls, n):
#         if n in cls._defaults:
#             return cls._defaults[n]
#         else:
#             return "Unrecognized attribute name '" + n + "'"

#     def __init__(self, **kwargs):
#         self.__dict__.update(self._defaults)  # 设置默认值
#         self.__dict__.update(kwargs)  # 更新用户覆盖的值
#         self.class_names = self._get_class()
#         self.anchors = self._get_anchors()
        
#         # 关键修复：TensorFlow 2.x 不再需要显式创建会话
#         # 移除会话创建代码，使用即时执行模式
#         self.sess = None  # 在 TF 2.x 中不再需要传统会话
        
#         self.boxes, self.scores, self.classes = self.generate()

#     def _get_class(self):
#         classes_path = os.path.expanduser(self.classes_path)
#         with open(classes_path) as f:
#             class_names = f.readlines()
#         class_names = [c.strip() for c in class_names]
#         return class_names

#     def _get_anchors(self):
#         anchors_path = os.path.expanduser(self.anchors_path)
#         with open(anchors_path) as f:
#             anchors = f.readline()
#         anchors = [float(x) for x in anchors.split(',')]
#         return np.array(anchors).reshape(-1, 2)

#     def generate(self):
#         model_path = os.path.expanduser(self.model_path)
#         assert model_path.endswith('.h5'), 'Keras模型或权重必须是.h5文件'

#         # 加载模型，或构造模型并加载权重
#         num_anchors = len(self.anchors)
#         num_classes = len(self.class_names)
#         is_tiny_version = num_anchors == 6  # 默认设置

#         try:
#             # 尝试加载模型
#             self.yolo_model = load_model(model_path, compile=False)
#         except:
#             # 如果加载失败，创建新模型并加载权重
#             if is_tiny_version:
#                 self.yolo_model = tiny_yolo_body(Input(shape=(None, None, 3)), num_anchors//2, num_classes)
#             else:
#                 self.yolo_model = yolo_body(Input(shape=(None, None, 3)), num_anchors//3, num_classes)
#             # 确保模型、锚点和类别匹配
#             self.yolo_model.load_weights(self.model_path)
#         else:
#             # 验证模型结构匹配
#             assert self.yolo_model.layers[-1].output_shape[-1] == \
#                    num_anchors / len(self.yolo_model.output) * (num_classes + 5), \
#                 '模型与给定的锚点和类别大小不匹配'

#         print('{} 模型、锚点和类别加载完成'.format(model_path))

#         # 生成绘制边界框的颜色
#         hsv_tuples = [(x / len(self.class_names), 1., 1.)
#                       for x in range(len(self.class_names))]
#         self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
#         self.colors = list(
#             map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
#                 self.colors))
#         np.random.seed(10101)  # 固定种子以确保运行间颜色一致
#         np.random.shuffle(self.colors)  # 打乱颜色以解相关相邻类别
#         np.random.seed(None)  # 重置种子为默认

#         # 关键修复：TensorFlow 2.x 使用即时执行，不需要 placeholder
#         # 移除 placeholder 相关代码
#         self.input_image_shape = tf.constant([416, 416], dtype=tf.float32)  # 使用常量代替 placeholder
        
#         # 修复多GPU支持 - 使用 TensorFlow 2.x 方式
#         if self.gpu_num >= 2:
#             try:
#                 # TensorFlow 2.x 的多GPU支持
#                 strategy = tf.distribute.MirroredStrategy()
#                 print('使用 {} 个GPU进行推理'.format(strategy.num_replicas_in_sync))
#                 # 注意：需要在策略范围内重新创建模型
#             except Exception as e:
#                 print("多GPU支持配置失败: {}, 使用单GPU模式".format(e))
        
#         # 关键修复：适配 TensorFlow 2.x 的 yolo_eval 调用方式
#         # 直接调用 yolo_eval，不需要 Lambda 层包装
#         boxes, scores, classes = yolo_eval(
#             self.yolo_model.output, self.anchors,
#             len(self.class_names), self.input_image_shape,
#             score_threshold=self.score, iou_threshold=self.iou
#         )
        
#         return boxes, scores, classes

#     def detect_image(self, image):
#         start = timer()

#         if self.model_image_size != (None, None):
#             assert self.model_image_size[0] % 32 == 0, '需要32的倍数'
#             assert self.model_image_size[1] % 32 == 0, '需要32的倍数'
#             boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
#         else:
#             new_image_size = (image.width - (image.width % 32),
#                               image.height - (image.height % 32))
#             boxed_image = letterbox_image(image, new_image_size)
#         image_data = np.array(boxed_image, dtype='float32')

#         print('输入图像形状:', image_data.shape)
#         image_data /= 255.
#         image_data = np.expand_dims(image_data, 0)  # 添加批次维度

#         # 关键修复：TensorFlow 2.x 使用即时执行，不需要会话
#         # 构建输入字典
#         feed_dict = {
#             self.yolo_model.input: image_data,
#             'input_image_shape': [image.size[1], image.size[0]]
#         }
        
#         # 直接使用模型预测
#         try:
#             # 方法1：使用模型的 __call__ 方法
#             predictions = self.yolo_model(image_data)
#             # 需要根据 yolo_eval 的返回结构处理 predictions
#             # 这里假设 yolo_eval 返回的是可以直接使用的张量
#             out_boxes, out_scores, out_classes = self.boxes, self.scores, self.classes
#         except Exception as e:
#             print("预测失败: {}, 使用备用方法".format(e))
#             # 备用方法：如果上述方法失败，使用传统方式
#             out_boxes, out_scores, out_classes = [], [], []

#         print('找到 {} 个边界框'.format(len(out_boxes) if out_boxes else 0))

#         font = ImageFont.truetype(font='font/FiraMono-Medium.otf',
#                     size=np.floor(3e-2 * image.size[1] + 0.5).astype('int32'))
#         thickness = (image.size[0] + image.size[1]) // 300

#         # 绘制检测结果
#         if out_boxes and len(out_boxes) > 0:
#             for i, c in reversed(list(enumerate(out_classes))):
#                 predicted_class = self.class_names[c]
#                 box = out_boxes[i]
#                 score = out_scores[i]

#                 label = '{} {:.2f}'.format(predicted_class, score)
#                 draw = ImageDraw.Draw(image)
#                 label_size = draw.textsize(label, font)

#                 top, left, bottom, right = box
#                 top = max(0, np.floor(top + 0.5).astype('int32'))
#                 left = max(0, np.floor(left + 0.5).astype('int32'))
#                 bottom = min(image.size[1], np.floor(bottom + 0.5).astype('int32'))
#                 right = min(image.size[0], np.floor(right + 0.5).astype('int32'))
#                 print(label, (left, top), (right, bottom))

#                 if top - label_size[1] >= 0:
#                     text_origin = np.array([left, top - label_size[1]])
#                 else:
#                     text_origin = np.array([left, top + 1])

#                 # 绘制边界框
#                 for i in range(thickness):
#                     draw.rectangle(
#                         [left + i, top + i, right - i, bottom - i],
#                         outline=self.colors[c])
#                 draw.rectangle(
#                     [tuple(text_origin), tuple(text_origin + label_size)],
#                     fill=self.colors[c])
#                 draw.text(text_origin, label, fill=(0, 0, 0), font=font)
#                 del draw

#         end = timer()
#         print('检测时间: {:.2f}秒'.format(end - start))
#         return image

#     def close_session(self):
#         # TensorFlow 2.x 中不需要显式关闭会话
#         if hasattr(self, 'sess') and self.sess is not None:
#             self.sess.close()
#         # 清理TensorFlow图
#         tf.keras.backend.clear_session()


# def detect_video(yolo, video_path, output_path=""):
#     import cv2
#     vid = cv2.VideoCapture(video_path)
#     if not vid.isOpened():
#         raise IOError("无法打开网络摄像头或视频")
#     video_FourCC = int(vid.get(cv2.CAP_PROP_FOURCC))
#     video_fps = vid.get(cv2.CAP_PROP_FPS)
#     video_size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
#                   int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#     isOutput = True if output_path != "" else False
#     if isOutput:
#         print("!!! 类型:", type(output_path), type(video_FourCC), type(video_fps), type(video_size))
#         out = cv2.VideoWriter(output_path, video_FourCC, video_fps, video_size)
#     accum_time = 0
#     curr_fps = 0
#     fps = "FPS: ??"
#     prev_time = timer()
#     while True:
#         return_value, frame = vid.read()
#         if not return_value:
#             break
#         image = Image.fromarray(frame)
#         image = yolo.detect_image(image)
#         result = np.asarray(image)
#         curr_time = timer()
#         exec_time = curr_time - prev_time
#         prev_time = curr_time
#         accum_time = accum_time + exec_time
#         curr_fps = curr_fps + 1
#         if accum_time > 1:
#             accum_time = accum_time - 1
#             fps = "FPS: " + str(curr_fps)
#             curr_fps = 0
#         cv2.putText(result, text=fps, org=(3, 15), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                     fontScale=0.50, color=(255, 0, 0), thickness=2)
#         cv2.namedWindow("结果", cv2.WINDOW_NORMAL)
#         cv2.imshow("结果", result)
#         if isOutput:
#             out.write(result)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     yolo.close_session()
#     if isOutput:
#         out.release()
#     cv2.destroyAllWindows()


# if __name__ == '__main__':
#     # 设置环境变量以减少日志输出
#     os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
#     # 创建YOLO检测器实例
#     yolo = YOLO()
    
#     try:
#         # 示例: 检测单张图片
#         image_path = "F:/data/VOC2007/test/11.jpg"
#         if os.path.exists(image_path):
#             image = Image.open(image_path)
#             result = yolo.detect_image(image)
#             result.show()
            
#             # 保存结果
#             result.save("F:/data/VOC2007/test/detection_result_11.jpg")
#             print("检测结果已保存")
#         else:
#             print("测试图片不存在: {}".format(image_path))
            
#     except Exception as e:
#         print("检测失败: {}".format(e))
#         import traceback
#         traceback.print_exc()
    
#     finally:
#         # 关闭会话
#         yolo.close_session()








# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 减少TensorFlow日志输出

# import tensorflow as tf
# import numpy as np
# import cv2
# from PIL import Image, ImageDraw, ImageFont
# import colorsys

# class SimpleYOLOv3:
#     def __init__(self, model_path, anchors_path, classes_path, input_size=416):
#         """
#         修复初始化顺序的简化版YOLOv3
#         Args:
#             model_path: 已训练好的.h5权重文件路径
#             anchors_path: 锚点文件路径
#             classes_path: 类别文件路径
#             input_size: 输入图像尺寸，默认416x416
#         """
#         self.model_path = model_path
#         self.anchors_path = anchors_path
#         self.classes_path = classes_path
#         self.input_size = input_size
        
#         # === 关键修复1：正确的初始化顺序 ===
#         # 先初始化基础配置，再加载模型
#         self.class_names = self._get_class_names()
#         self.anchors = self._get_anchors()
#         self.colors = self._generate_colors()
        
#         print(f"基础配置加载完成: {len(self.class_names)}个类别, {len(self.anchors)}个锚点")
        
#         # 然后加载模型
#         self.model = self._load_model()
        
#         print(f"YOLOv3模型加载完成: 输入尺寸{input_size}x{input_size}")

#     def _load_model(self):
#         """加载训练好的YOLOv3模型"""
#         try:
#             # 尝试直接加载完整模型
#             model = tf.keras.models.load_model(self.model_path, compile=False)
#             print(f"完整模型从 {self.model_path} 加载成功")
#             return model
#         except Exception as e:
#             print(f"完整模型加载失败: {e}，尝试创建模型结构并加载权重...")
#             return self._create_and_load_model()

#     def _create_and_load_model(self):
#         """创建模型结构并加载权重（备用方案）"""
#         try:
#             # 动态导入，避免循环依赖
#             from yolo3.model import yolo_body, tiny_yolo_body
            
#             num_anchors = len(self.anchors)
#             num_classes = len(self.class_names)
#             is_tiny_version = num_anchors == 6  # tiny版本有6个锚点
            
#             print(f"创建模型结构: {'YOLOv3-tiny' if is_tiny_version else 'YOLOv3'}")
            
#             # 创建模型结构
#             input_layer = tf.keras.layers.Input(shape=(None, None, 3))
            
#             if is_tiny_version:
#                 model = tiny_yolo_body(input_layer, num_anchors//2, num_classes)
#             else:
#                 model = yolo_body(input_layer, num_anchors//3, num_classes)
            
#             # 加载权重
#             print(f"加载权重文件: {self.model_path}")
#             model.load_weights(self.model_path)
#             print("模型结构创建和权重加载成功")
#             return model
            
#         except ImportError as e:
#             print(f"无法导入模型构建模块: {e}")
#             raise
#         except Exception as e:
#             print(f"模型创建或权重加载失败: {e}")
#             # 最后尝试：使用OpenCV的DNN模块
#             return self._create_opencv_model()

#     def _create_opencv_model(self):
#         """使用OpenCV DNN模块作为备用方案"""
#         print("尝试使用OpenCV DNN模块加载模型...")
#         try:
#             # 这里可以实现OpenCV DNN的加载逻辑
#             # 由于不知道您的具体模型格式，这里返回None
#             print("OpenCV DNN加载需要额外的模型文件配置")
#             return None
#         except Exception as e:
#             print(f"OpenCV DNN加载也失败: {e}")
#             raise

#     def _get_anchors(self):
#         """从文件加载锚点"""
#         try:
#             anchors_path = os.path.expanduser(self.anchors_path)
#             with open(anchors_path, 'r') as f:
#                 anchors_line = f.readline().strip()
#             anchors = [float(x) for x in anchors_line.split(',')]
#             return np.array(anchors).reshape(-1, 2)
#         except Exception as e:
#             print(f"加载锚点文件失败: {e}")
#             # 返回默认的YOLOv3锚点
#             return np.array([[10,13], [16,30], [33,23], [30,61], [62,45], 
#                            [59,119], [116,90], [156,198], [373,326]])

#     def _get_class_names(self):
#         """从文件加载类别名称"""
#         try:
#             classes_path = os.path.expanduser(self.classes_path)
#             with open(classes_path, 'r') as f:
#                 class_names = [line.strip() for line in f.readlines()]
#             return class_names
#         except Exception as e:
#             print(f"加载类别文件失败: {e}")
#             # 返回默认的COCO类别
#             return ['person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck']

#     def _generate_colors(self):
#         """为每个类别生成distinct颜色"""
#         hsv_tuples = [(x / len(self.class_names), 1., 1.) 
#                       for x in range(len(self.class_names))]
#         colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
#         colors = list(map(lambda x: 
#                          (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), 
#                          colors))
#         return colors

#     def preprocess_image(self, image):
#         """图像预处理"""
#         # 调整图像大小并填充为正方形
#         image_resized = self.letterbox_image(image, (self.input_size, self.input_size))
        
#         # 转换为numpy数组并归一化
#         image_array = np.array(image_resized, dtype='float32') / 255.0
        
#         # 添加批次维度
#         image_array = np.expand_dims(image_array, 0)
        
#         return image_array, image.size

#     def letterbox_image(self, image, size):
#         """保持宽高比调整图像大小并在边缘填充"""
#         iw, ih = image.size
#         w, h = size
#         scale = min(w/iw, h/ih)
#         nw = int(iw * scale)
#         nh = int(ih * scale)

#         image = image.resize((nw, nh), Image.BICUBIC)
#         new_image = Image.new('RGB', size, (128, 128, 128))
#         new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
#         return new_image

#     def predict(self, image_array):
#         """使用模型进行预测"""
#         if self.model is None:
#             print("模型未正确加载，无法进行预测")
#             return None
#         return self.model.predict(image_array)

#     def yolo_head(self, feats, anchors, num_classes, input_shape, calc_loss=False):
#         """将最终特征图转换为边界框参数"""
#         pass  # 需要根据您的具体模型实现

#     def yolo_correct_boxes(self, box_xy, box_wh, input_shape, image_shape):
#         """修正边界框坐标"""
#         pass  # 需要根据您的具体模型实现

#     def yolo_boxes_and_scores(self, feats, anchors, num_classes, input_shape, image_shape):
#         """从特征图中提取框和分数"""
#         pass  # 需要根据您的具体模型实现

#     def yolo_eval(self, yolo_outputs, anchors, num_classes, image_shape, 
#                  max_boxes=20, score_threshold=0.3, iou_threshold=0.45):
#         """评估YOLO输出并返回边界框"""
#         pass  # 需要根据您的具体模型实现

#     def postprocess(self, predictions, original_size, score_threshold=0.3, iou_threshold=0.45):
#         """后处理：解码边界框并应用非极大值抑制"""
#         # 简化版后处理 - 需要根据您的模型输出格式调整
#         boxes = []
#         scores = []
#         classes = []
        
#         # 这里需要根据您的模型实际输出结构进行解析
#         if predictions is not None:
#             print(f"模型输出类型: {type(predictions)}, 形状: {getattr(predictions, 'shape', 'Unknown')}")
            
#             # 如果是多输出模型
#             if isinstance(predictions, (list, tuple)):
#                 for i, pred in enumerate(predictions):
#                     print(f"输出 {i}: 形状 {pred.shape}")
#             else:
#                 # 单输出模型
#                 print(f"单一输出形状: {predictions.shape}")
        
#         # 返回空结果，您需要根据实际模型输出实现具体的解码逻辑
#         return np.array(boxes), np.array(scores), np.array(classes)

#     def draw_detections(self, image, boxes, scores, classes, original_size, confidence_threshold=0.3):
#         """在图像上绘制检测结果"""
#         draw = ImageDraw.Draw(image)
        
#         # 尝试加载字体
#         try:
#             font = ImageFont.truetype('arial.ttf', 20)
#         except:
#             try:
#                 font = ImageFont.load_default()
#             except:
#                 font = None
        
#         im_width, im_height = original_size
#         detection_count = 0
        
#         for i, (box, score, class_id) in enumerate(zip(boxes, scores, classes)):
#             if score < confidence_threshold:
#                 continue
                
#             detection_count += 1
            
#             # 确保class_id是整数
#             class_id = int(class_id)
#             if class_id >= len(self.class_names):
#                 print(f"警告: 类别ID {class_id} 超出范围，最大为 {len(self.class_names)-1}")
#                 continue
                
#             predicted_class = self.class_names[class_id]
            
#             # 解码边界框坐标
#             if len(box) == 4:  # x1, y1, x2, y2 格式
#                 y1, x1, y2, x2 = box
#             else:
#                 # 默认处理
#                 x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
            
#             # 缩放回原图尺寸
#             x1 = int(x1 * im_width)
#             y1 = int(y1 * im_height)
#             x2 = int(x2 * im_width)
#             y2 = int(y2 * im_height)
            
#             # 确保坐标在图像范围内
#             x1 = max(0, min(x1, im_width-1))
#             y1 = max(0, min(y1, im_height-1))
#             x2 = max(0, min(x2, im_width-1))
#             y2 = max(0, min(y2, im_height-1))
            
#             # 选择颜色
#             color = self.colors[class_id % len(self.colors)]
            
#             # 绘制边界框
#             draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            
#             # 绘制标签
#             label = f"{predicted_class}: {score:.2f}"
            
#             if font:
#                 label_size = draw.textsize(label, font=font)
                
#                 # 标签背景
#                 draw.rectangle([x1, y1-label_size[1]-5, x1+label_size[0], y1], fill=color)
#                 # 标签文字
#                 draw.text((x1, y1-label_size[1]-5), label, fill=(0, 0, 0), font=font)
#             else:
#                 # 简单文本
#                 draw.text((x1, y1-15), label, fill=color)
            
#             print(f"检测到: {label} 位置: ({x1}, {y1}, {x2}, {y2})")
        
#         print(f"总共检测到 {detection_count} 个目标")
#         return image

#     def detect_image(self, image_path, output_path=None, confidence_threshold=0.3):
#         """检测单张图片"""
#         # 加载图像
#         try:
#             image = Image.open(image_path)
#             print(f"加载图像: {image_path}, 尺寸: {image.size}")
#         except Exception as e:
#             print(f"无法加载图像 {image_path}: {e}")
#             return None
        
#         # 预处理
#         image_array, original_size = self.preprocess_image(image)
        
#         # 预测
#         print("进行预测...")
#         try:
#             predictions = self.predict(image_array)
            
#             if predictions is None:
#                 print("预测失败，模型未正确加载")
#                 return image
            
#             # 后处理
#             boxes, scores, classes = self.postprocess(predictions, original_size, confidence_threshold)
            
#             # 绘制结果
#             result_image = self.draw_detections(image, boxes, scores, classes, original_size, confidence_threshold)
            
#             # 保存结果
#             if output_path:
#                 # 确保输出目录存在
#                 os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
#                 result_image.save(output_path)
#                 print(f"结果已保存至: {output_path}")
            
#             return result_image
            
#         except Exception as e:
#             print(f"预测过程出错: {e}")
#             import traceback
#             traceback.print_exc()
#             return image

#     def close(self):
#         """清理资源"""
#         if hasattr(self, 'model') and self.model is not None:
#             tf.keras.backend.clear_session()
#             print("模型资源已清理")


# # 使用示例
# def main():
#     # 配置路径 - 请根据您的实际路径修改
#     config = {
#         "model_path": "F:/data/VOC2007/logs/000/ep018-loss63.362.weights.h5",
#         "anchors_path": "F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/yolo_anchors.txt", 
#         "classes_path": "F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/coco_classes.txt",
#         "input_size": 416
#     }
    
#     try:
#         # 创建YOLOv3检测器
#         yolo = SimpleYOLOv3(
#             model_path=config["model_path"],
#             anchors_path=config["anchors_path"],
#             classes_path=config["classes_path"],
#             input_size=config["input_size"]
#         )
        
#         # 检测单张图片
#         # image_path = "F:/data/VOC2007/test/192.jpg"
#         image_path = "F:/data/VOC2007/JPEGImages/190.jpg"
#         output_path = "F:/data/VOC2007/test/detection_result_190.jpg"
        
#         if os.path.exists(image_path):
#             result = yolo.detect_image(image_path, output_path, confidence_threshold=0.3)
#             if result:
#                 result.show()  # 显示结果
#                 print("检测完成!")
#             else:
#                 print("检测失败")
#         else:
#             print(f"测试图片不存在: {image_path}")
#             # 可以在这里创建一个测试图像
#             print("请确保图片路径正确")
            
#     except Exception as e:
#         print(f"初始化或检测失败: {e}")
#         import traceback
#         traceback.print_exc()
    
#     finally:
#         # 清理资源
#         if 'yolo' in locals():
#             yolo.close()


# if __name__ == "__main__":
#     main()





import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import colorsys

class SimpleYOLOv3:
    def __init__(self, model_path, anchors_path, classes_path, input_size=416):
        """修复后的YOLOv3检测器"""
        self.model_path = model_path
        self.anchors_path = anchors_path
        self.classes_path = classes_path
        self.input_size = input_size
        
        # 初始化基础配置
        self.class_names = self._get_class_names()
        self.anchors = self._get_anchors()
        self.colors = self._generate_colors()
        
        print(f"基础配置加载完成: {len(self.class_names)}个类别, {len(self.anchors)}个锚点")
        
        # 加载模型
        self.model = self._load_model()
        print(f"YOLOv3模型加载完成: 输入尺寸{input_size}x{input_size}")

    def _load_model(self):
        """加载训练好的YOLOv3模型"""
        try:
            model = tf.keras.models.load_model(self.model_path, compile=False)
            print(f"完整模型从 {self.model_path} 加载成功")
            return model
        except Exception as e:
            print(f"完整模型加载失败: {e}，尝试创建模型结构并加载权重...")
            return self._create_and_load_model()

    def _create_and_load_model(self):
        """创建模型结构并加载权重"""
        try:
            from yolo3.model import yolo_body, tiny_yolo_body
            
            num_anchors = len(self.anchors)
            num_classes = len(self.class_names)
            is_tiny_version = num_anchors == 6
            
            print(f"创建模型结构: {'YOLOv3-tiny' if is_tiny_version else 'YOLOv3'}")
            
            input_layer = tf.keras.layers.Input(shape=(None, None, 3))
            
            if is_tiny_version:
                model = tiny_yolo_body(input_layer, num_anchors//2, num_classes)
            else:
                model = yolo_body(input_layer, num_anchors//3, num_classes)
            
            model.load_weights(self.model_path)
            print("模型结构创建和权重加载成功")
            return model
            
        except Exception as e:
            print(f"模型创建失败: {e}")
            raise

    def _get_anchors(self):
        """从文件加载锚点"""
        try:
            anchors_path = os.path.expanduser(self.anchors_path)
            with open(anchors_path, 'r') as f:
                anchors_line = f.readline().strip()
            anchors = [float(x) for x in anchors_line.split(',')]
            return np.array(anchors).reshape(-1, 2)
        except Exception as e:
            print(f"加载锚点文件失败: {e}")
            return np.array([[10,13], [16,30], [33,23], [30,61], [62,45], 
                           [59,119], [116,90], [156,198], [373,326]])

    def _get_class_names(self):
        """从文件加载类别名称"""
        try:
            classes_path = os.path.expanduser(self.classes_path)
            with open(classes_path, 'r') as f:
                class_names = [line.strip() for line in f.readlines()]
            return class_names
        except Exception as e:
            print(f"加载类别文件失败: {e}")
            return ['person']

    def _generate_colors(self):
        """为每个类别生成distinct颜色"""
        hsv_tuples = [(x / len(self.class_names), 1., 1.) 
                      for x in range(len(self.class_names))]
        colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(map(lambda x: 
                         (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)), 
                         colors))
        return colors

    def preprocess_image(self, image):
        """图像预处理"""
        image_resized = self.letterbox_image(image, (self.input_size, self.input_size))
        image_array = np.array(image_resized, dtype='float32') / 255.0
        image_array = np.expand_dims(image_array, 0)
        return image_array, image.size

    def letterbox_image(self, image, size):
        """保持宽高比调整图像大小并在边缘填充"""
        iw, ih = image.size
        w, h = size
        scale = min(w/iw, h/ih)
        nw = int(iw * scale)
        nh = int(ih * scale)

        image = image.resize((nw, nh), Image.BICUBIC)
        new_image = Image.new('RGB', size, (128, 128, 128))
        new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))
        return new_image

    def predict(self, image_array):
        """使用模型进行预测"""
        return self.model.predict(image_array)

    def decode_yolo_predictions(self, predictions, image_shape, confidence_threshold=0.01):
        """解码YOLOv3模型输出"""
        boxes = []
        scores = []
        class_ids = []
        
        if predictions is None:
            return boxes, scores, class_ids
        
        for scale_idx, pred in enumerate(predictions):
            print(f"解码尺度 {scale_idx}: 形状 {pred.shape}")
            
            grid_h, grid_w = pred.shape[1:3]
            
            if scale_idx == 0:
                anchors = self.anchors[6:9] if len(self.anchors) >= 9 else self.anchors[0:3]
            elif scale_idx == 1:
                anchors = self.anchors[3:6] if len(self.anchors) >= 6 else self.anchors[0:3]
            else:
                anchors = self.anchors[0:3]
            
            pred = pred.reshape((1, grid_h, grid_w, len(anchors), -1))
            
            for h in range(grid_h):
                for w in range(grid_w):
                    for a in range(len(anchors)):
                        box_pred = pred[0, h, w, a]
                        tx, ty, tw, th, confidence = box_pred[0:5]
                        class_probs = box_pred[5:]
                        
                        tx = 1 / (1 + np.exp(-tx))
                        ty = 1 / (1 + np.exp(-ty))
                        confidence = 1 / (1 + np.exp(-confidence))
                        
                        class_probs = np.exp(class_probs - np.max(class_probs))
                        class_probs = class_probs / np.sum(class_probs)
                        class_id = np.argmax(class_probs)
                        class_score = class_probs[class_id]
                        
                        final_score = confidence * class_score
                        
                        if final_score < confidence_threshold:
                            continue
                        
                        bx = (tx + w) / grid_w
                        by = (ty + h) / grid_h
                        bw = anchors[a][0] * np.exp(tw) / self.input_size
                        bh = anchors[a][1] * np.exp(th) / self.input_size
                        
                        x1 = bx - bw / 2
                        y1 = by - bh / 2
                        x2 = bx + bw / 2
                        y2 = by + bh / 2
                        
                        x1 = int(x1 * image_shape[0])
                        y1 = int(y1 * image_shape[1])
                        x2 = int(x2 * image_shape[0])
                        y2 = int(y2 * image_shape[1])
                        
                        x1 = max(0, min(x1, image_shape[0]-1))
                        y1 = max(0, min(y1, image_shape[1]-1))
                        x2 = max(0, min(x2, image_shape[0]-1))
                        y2 = max(0, min(y2, image_shape[1]-1))
                        
                        boxes.append([x1, y1, x2, y2])
                        scores.append(final_score)
                        class_ids.append(class_id)
        
        return np.array(boxes), np.array(scores), np.array(class_ids)

    def non_max_suppression(self, boxes, scores, class_ids, iou_threshold=0.45, max_output_size=100):
        """实现非极大值抑制 (NMS)"""
        if len(boxes) == 0:
            return boxes, scores, class_ids
        
        indices = np.argsort(scores)[::-1]
        boxes = boxes[indices]
        scores = scores[indices]
        class_ids = class_ids[indices]
        
        keep_boxes = []
        keep_scores = []
        keep_class_ids = []
        
        while len(indices) > 0:
            current_idx = indices[0]
            keep_boxes.append(boxes[current_idx])
            keep_scores.append(scores[current_idx])
            keep_class_ids.append(class_ids[current_idx])
            
            if len(keep_boxes) >= max_output_size:
                break
            
            current_box = boxes[current_idx]
            other_boxes = boxes[indices[1:]]
            
            x1 = np.maximum(current_box[0], other_boxes[:, 0])
            y1 = np.maximum(current_box[1], other_boxes[:, 1])
            x2 = np.minimum(current_box[2], other_boxes[:, 2])
            y2 = np.minimum(current_box[3], other_boxes[:, 3])
            
            intersection = np.maximum(0, x2 - x1) * np.maximum(0, y2 - y1)
            area_current = (current_box[2] - current_box[0]) * (current_box[3] - current_box[1])
            area_others = (other_boxes[:, 2] - other_boxes[:, 0]) * (other_boxes[:, 3] - other_boxes[:, 1])
            union = area_current + area_others - intersection
            
            iou = intersection / (union + 1e-8)
            
            keep_indices = np.where(iou <= iou_threshold)[0]
            indices = indices[keep_indices + 1]
        
        return np.array(keep_boxes), np.array(keep_scores), np.array(keep_class_ids)

    def postprocess(self, predictions, original_size, confidence_threshold=0.01, iou_threshold=0.45):
        """完整的后处理流程"""
        print("开始后处理...")
        
        boxes, scores, class_ids = self.decode_yolo_predictions(
            predictions, original_size, confidence_threshold
        )
        
        print(f"解码后检测框数量: {len(boxes)}")
        
        if len(boxes) == 0:
            print("没有检测到任何目标")
            return boxes, scores, class_ids
        
        boxes, scores, class_ids = self.non_max_suppression(
            boxes, scores, class_ids, iou_threshold
        )
        
        print(f"NMS后检测框数量: {len(boxes)}")
        return boxes, scores, class_ids

    def draw_detections(self, image, boxes, scores, classes, original_size, confidence_threshold=0.3):
        """在图像上绘制检测结果 - 修复textsize问题"""
        if len(boxes) == 0:
            print("没有检测到目标，无需绘制")
            return image
            
        draw = ImageDraw.Draw(image)
        
        # 尝试加载字体
        try:
            font = ImageFont.truetype('arial.ttf', 20)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        im_width, im_height = original_size
        detection_count = 0
        
        for i, (box, score, class_id) in enumerate(zip(boxes, scores, classes)):
            if score < confidence_threshold:
                continue
                
            detection_count += 1
            class_id = int(class_id)
            
            if class_id >= len(self.class_names):
                print(f"警告: 类别ID {class_id} 超出范围")
                class_name = f"class_{class_id}"
            else:
                class_name = self.class_names[class_id]
            
            x1, y1, x2, y2 = [int(coord) for coord in box]
            
            x1 = max(0, min(x1, im_width-1))
            y1 = max(0, min(y1, im_height-1))
            x2 = max(0, min(x2, im_width-1))
            y2 = max(0, min(y2, im_height-1))
            
            color = self.colors[class_id % len(self.colors)]
            
            # 绘制边界框
            draw.rectangle([x1, y1, x2, y2], outline=color, width=3)
            
            # 绘制标签
            label = "Cat Face"
            
            if font:
                # === 关键修复：兼容不同Pillow版本的文本尺寸获取 ===
                try:
                    # 方法1: 使用textbbox (Pillow 9.0.0+)
                    bbox = draw.textbbox((0, 0), label, font=font)
                    label_width = bbox[2] - bbox[0]
                    label_height = bbox[3] - bbox[1]
                except AttributeError:
                    try:
                        # 方法2: 使用textsize (Pillow 旧版本)
                        label_width, label_height = draw.textsize(label, font=font)
                    except AttributeError:
                        # 方法3: 使用字体对象的getbbox方法
                        try:
                            bbox = font.getbbox(label)
                            label_width = bbox[2] - bbox[0]
                            label_height = bbox[3] - bbox[1]
                        except:
                            # 方法4: 估算尺寸
                            label_width = len(label) * 10
                            label_height = 20
                
                # 确保标签在图像范围内
                label_x = x1
                label_y = y1 - label_height - 5
                
                # 调整标签位置如果超出上边界
                if label_y < 0:
                    label_y = y1 + 5
                
                # 标签背景
                draw.rectangle([label_x, label_y, label_x + label_width, label_y + label_height], fill=color)
                # 标签文字
                draw.text((label_x, label_y), label, fill=(0, 0, 0), font=font)
            else:
                # 简单文本
                draw.text((x1, y1-15), label, fill=color)
            
            print(f"检测到: {label} 位置: ({x1}, {y1}, {x2}, {y2})")
        
        print(f"总共绘制 {detection_count} 个检测结果")
        return image

    def detect_image(self, image_path, output_path=None, confidence_threshold=0.01):
        """检测单张图片"""
        try:
            image = Image.open(image_path)
            print(f"加载图像: {image_path}, 尺寸: {image.size}")
        except Exception as e:
            print(f"无法加载图像 {image_path}: {e}")
            return None
        
        # 预处理
        image_array, original_size = self.preprocess_image(image)
        
        # 预测
        print("进行预测...")
        predictions = self.predict(image_array)
        
        if predictions is None:
            print("预测失败")
            return image
        
        # 后处理
        boxes, scores, classes = self.postprocess(
            predictions, 
            (image.size[0], image.size[1]),
            confidence_threshold=confidence_threshold,
            iou_threshold=0.45
        )
        
        # 绘制结果
        result_image = self.draw_detections(
            image, boxes, scores, classes, image.size, confidence_threshold
        )
        
        # 保存结果
        if output_path:
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            result_image.save(output_path)
            print(f"结果已保存至: {output_path}")
        
        return result_image

    def close(self):
        """清理资源"""
        if hasattr(self, 'model') and self.model is not None:
            tf.keras.backend.clear_session()
            print("模型资源已清理")


def main():
    """主测试函数"""
    config = {
        "model_path": "F:/data/VOC2007/logs/000/ep090-loss27.397.weights.h5",
        "anchors_path": "F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/yolo_anchors.txt",
        "classes_path": "F:/PycharmProjects/pythonProject/大四上/专项课程/keras-yolo3-master/model_data/coco_classes.txt",
        "input_size": 416
    }
    
    try:
        yolo = SimpleYOLOv3(**config)
        
        # 测试不同的置信度阈值
        test_thresholds = [0.008, 0.009, 0.02]
        
        for threshold in test_thresholds:
            print(f"\n{'='*50}")
            print(f"测试置信度阈值: {threshold}")
            print(f"{'='*50}")
            
            image_path = "F:/data/VOC2007/JPEGImages/192.jpg"
            output_path = f"F:/data/VOC2007/test/detection_result_192_second_thresh{threshold}.jpg"
            
            if os.path.exists(image_path):
                result = yolo.detect_image(image_path, output_path, confidence_threshold=threshold)
                if result is not None:
                    result.show()
                    print(f"阈值 {threshold}: 检测完成")
                else:
                    print(f"阈值 {threshold}: 检测失败")
            else:
                print(f"测试图片不存在: {image_path}")
                
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'yolo' in locals():
            yolo.close()


if __name__ == "__main__":
    main()