import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from mtcnn import MTCNN

# 检查TensorFlow版本并设置兼容性
if tf.__version__.startswith('2'):
    tf = tf.compat.v1
    tf.disable_v2_behavior()

# 全局参数设置
WEIGHT_INIT = 0.01
USE_BN = True
color = (0, 255, 0)  # 绿色标注框

def _conv(name, x, filter_size, in_filters, out_filters, strides):
    """定义卷积层"""
    with tf.variable_scope(name):
        filter = tf.get_variable('DW', [filter_size, filter_size, in_filters, out_filters], tf.float32,
                                tf.random_normal_initializer(stddev=WEIGHT_INIT))
        return tf.nn.conv2d(x, filter, [1, strides, strides, 1], 'SAME')

def _relu(x, leakiness=0.0):
    """Leaky ReLU激活函数"""
    return tf.where(tf.less(x, 0.0), leakiness * x, x, name='leaky_relu')

def _FC(name, x, out_dim, keep_rate, activation='relu'):
    """全连接层"""
    assert activation in ['relu', 'softmax', 'linear']
    with tf.variable_scope(name):
        dim = x.get_shape().as_list()
        dim = np.prod(dim[1:])
        x = tf.reshape(x, [-1, dim])
        W = tf.get_variable('DW', [x.get_shape()[1], out_dim],
                           initializer=tf.random_normal_initializer(stddev=WEIGHT_INIT))
        b = tf.get_variable('bias', [out_dim], initializer=tf.constant_initializer())
        x = tf.nn.xw_plus_b(x, W, b)
        
        if activation == 'relu':
            x = _relu(x)
            return tf.nn.dropout(x, keep_rate)
        elif activation == 'softmax':
            return tf.nn.softmax(x)
        else:
            return x

def _max_pool(x, filter_size, stride):
    """最大池化层"""
    return tf.nn.max_pool(x, [1, filter_size, filter_size, 1], [1, stride, stride, 1], 'SAME')

def batch_norm(x, n_out, phase_train=True, scope='bn'):
    """批归一化层"""
    with tf.variable_scope(scope):
        beta = tf.Variable(tf.constant(0.0, shape=[n_out]), name='beta', trainable=True)
        gamma = tf.Variable(tf.constant(1.0, shape=[n_out]), name='gamma', trainable=True)
        batch_mean, batch_var = tf.nn.moments(x, [0, 1, 2], name='moments')
        ema = tf.train.ExponentialMovingAverage(decay=0.5)
        
        def mean_var_with_update():
            ema_apply_op = ema.apply([batch_mean, batch_var])
            with tf.control_dependencies([ema_apply_op]):
                return tf.identity(batch_mean), tf.identity(batch_var)
        
        mean, var = tf.cond(phase_train,
                           mean_var_with_update,
                           lambda: (ema.average(batch_mean), ema.average(batch_var)))
        normed = tf.nn.batch_normalization(x, mean, var, beta, gamma, 1e-3)
        return normed

def VGG_ConvBlock(name, x, in_filters, out_filters, repeat, strides, phase_train):
    """VGG卷积块"""
    with tf.variable_scope(name):
        for layer in range(repeat):
            scope_name = name + '_' + str(layer)
            x = _conv(scope_name, x, 3, in_filters, out_filters, strides)
            if USE_BN:
                x = batch_norm(x, out_filters, phase_train)
            x = _relu(x)
            in_filters = out_filters
        x = _max_pool(x, 2, 2)
        return x

def BKNetModel(x):
    """人脸分析主网络结构"""
    phase_train = tf.placeholder(tf.bool)
    keep_prob = tf.placeholder(tf.float32)
    
    # 共享特征提取层
    x = VGG_ConvBlock('Block1', x, 1, 32, 2, 1, phase_train)
    x = VGG_ConvBlock('Block2', x, 32, 64, 2, 1, phase_train)
    x = VGG_ConvBlock('Block3', x, 64, 128, 2, 1, phase_train)
    x = VGG_ConvBlock('Block4', x, 128, 256, 3, 1, phase_train)
    
    # 表情分支
    smile_fc1 = _FC('smile_fc1', x, 256, keep_prob)
    smile_fc2 = _FC('smile_fc2', smile_fc1, 256, keep_prob)
    y_smile_conv = _FC('smile_softmax', smile_fc2, 2, keep_prob, 'softmax')
    
    # 性别分支
    gender_fc1 = _FC('gender_fc1', x, 256, keep_prob)
    gender_fc2 = _FC('gender_fc2', gender_fc1, 256, keep_prob)
    y_gender_conv = _FC('gender_softmax', gender_fc2, 2, keep_prob, 'softmax')
    
    # 年龄分支
    age_fc1 = _FC('age_fc1', x, 256, keep_prob)
    age_fc2 = _FC('age_fc2', age_fc1, 256, keep_prob)
    y_age_conv = _FC('age_softmax', age_fc2, 101, keep_prob, 'softmax')
    
    return y_smile_conv, y_gender_conv, y_age_conv, phase_train, keep_prob

def load_network():
    """加载预训练模型"""
    # 使用tf.compat.v1兼容TensorFlow 2.x
    sess = tf.Session()
    x = tf.placeholder(tf.float32, [None, 48, 48, 1])
    y_smile_conv, y_gender_conv, y_age_conv, phase_train, keep_prob = BKNetModel(x)
    saver = tf.compat.v1.train.Saver()
    
    try:
        saver.restore(sess, '/opt/data/face/model-age101.ckpt')
    except:
        # 尝试不同的模型文件路径
        try:
            saver.restore(sess, '/opt/data/face/model-age101.ckpt.index')
        except:
            print("模型文件不存在，请下载预训练模型")
            return None, None, None, None, None, None, None
    
    return sess, x, y_smile_conv, y_gender_conv, y_age_conv, phase_train, keep_prob

def draw_label(image, x, y, w, h, label, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, thickness=2):
    """绘制检测框和标签"""
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
    cv2.putText(image, label, (x, y - 10), font, font_scale, color, thickness)

def predict_face(img_path):
    """人脸分析主函数"""
    # 加载模型
    result = load_network()
    if result[0] is None:
        return
    
    sess, x, y_smile_conv, y_gender_conv, y_age_conv, phase_train, keep_prob = result
    
    # 初始化MTCNN检测器
    detector = MTCNN()
    
    # 读取图像
    original_img = cv2.imread(img_path)
    if original_img is None:
        print(f"无法读取图像: {img_path}")
        return
    
    # 人脸检测
    results = detector.detect_faces(original_img)
    
    if not results:
        print("未检测到人脸")
        plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()
        return
    
    # 对每个检测到的人脸进行分析
    for i, result in enumerate(results):
        bounding_box = result['box']
        keypoints = result['keypoints']
        
        x_coordinate, y_coordinate, w_coordinate, h_coordinate = bounding_box
        
        # 确保坐标不越界
        x_coordinate = max(0, x_coordinate)
        y_coordinate = max(0, y_coordinate)
        w_coordinate = min(w_coordinate, original_img.shape[1] - x_coordinate)
        h_coordinate = min(h_coordinate, original_img.shape[0] - y_coordinate)
        
        # 提取人脸区域
        face_img = original_img[y_coordinate:y_coordinate+h_coordinate, 
                               x_coordinate:x_coordinate+w_coordinate]
        
        if face_img.size == 0:
            continue
            
        # 预处理
        gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        resized_face = cv2.resize(gray_face, (48, 48))
        normalized_face = (resized_face - 128) / 255.0
        
        # 准备输入数据
        T = np.zeros([48, 48, 1])
        T[:, :, 0] = normalized_face
        test_img = np.asarray([T])
        
        # 预测
        smile_pred = sess.run(y_smile_conv, feed_dict={x: test_img, phase_train: False, keep_prob: 1.0})
        gender_pred = sess.run(y_gender_conv, feed_dict={x: test_img, phase_train: False, keep_prob: 1.0})
        age_pred = sess.run(y_age_conv, feed_dict={x: test_img, phase_train: False, keep_prob: 1.0})
        
        # 解析结果
        smile_label = ":-)" if np.argmax(smile_pred) == 1 else "-_-"
        gender_label = "Female" if np.argmax(gender_pred) == 0 else "Male"
        age_label = str(np.argmax(age_pred))
        
        # 绘制结果
        label = f"Smile: {smile_label}, Gender: {gender_label}, Age: {age_label}"
        draw_label(original_img, x_coordinate, y_coordinate, w_coordinate, h_coordinate, label)
        
        # 绘制关键点
        for keypoint in keypoints.values():
            cv2.circle(original_img, keypoint, 2, color, 2)
    
    # 显示结果
    plt.figure(figsize=(12, 8))
    plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title('Face Analysis Result')
    plt.show()

# 使用示例
if __name__ == "__main__":
    # 测试单张图像
    image_path = "test_face.jpg"  # 替换为你的图像路径
    predict_face(image_path)