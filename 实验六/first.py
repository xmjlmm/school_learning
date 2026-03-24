import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from mtcnn import MTCNN

# 初始化MTCNN人脸检测器
detector = MTCNN()

# 定义网络参数
WEIGHT_INIT = 0.01
USE_BN = True

# 定义工具函数
def _conv(name, x, filter_size, in_filters, out_filters, strides):
    with tf.variable_scope(name):
        n = filter_size * filter_size * out_filters
        filter = tf.get_variable('DW', [filter_size, filter_size, in_filters, out_filters], 
                                tf.float32, tf.random_normal_initializer(stddev=WEIGHT_INIT))
        return tf.nn.conv2d(x, filter, [1, strides, strides, 1], 'SAME')

def _relu(x, leakiness=0.0):
    return tf.where(tf.less(x, 0.0), leakiness * x, x, name='leaky_relu')

def _FC(name, x, out_dim, keep_rate, activation='relu'):
    assert (activation == 'relu') or (activation == 'softmax') or (activation == 'linear')
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
        elif activation == 'softmax':
            x = tf.nn.softmax(x)
        if activation != 'relu':
            return x
        else:
            return tf.nn.dropout(x, keep_rate)

def _max_pool(x, filter_size, stride):
    return tf.nn.max_pool(x, [1, filter_size, filter_size, 1], [1, stride, stride, 1], 'SAME')

def batch_norm(x, n_out, phase_train=True, scope='bn'):
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
    phase_train = tf.placeholder(tf.bool)
    keep_prob = tf.placeholder(tf.float32)
    
    x = VGG_ConvBlock('Block1', x, 1, 32, 2, 1, phase_train)
    x = VGG_ConvBlock('Block2', x, 32, 64, 2, 1, phase_train)
    x = VGG_ConvBlock('Block3', x, 64, 128, 2, 1, phase_train)
    x = VGG_ConvBlock('Block4', x, 128, 256, 3, 1, phase_train)
    
    # Smile branch
    smile_fc1 = _FC('smile_fc1', x, 256, keep_prob)
    smile_fc2 = _FC('smile_fc2', smile_fc1, 256, keep_prob)
    y_smile_conv = _FC('smile_softmax', smile_fc2, 2, keep_prob, 'softmax')
    
    # Gender branch
    gender_fc1 = _FC('gender_fc1', x, 256, keep_prob)
    gender_fc2 = _FC('gender_fc2', gender_fc1, 256, keep_prob)
    y_gender_conv = _FC('gender_softmax', gender_fc2, 2, keep_prob, 'softmax')
    
    # Age branch
    age_fc1 = _FC('age_fc1', x, 256, keep_prob)
    age_fc2 = _FC('age_fc2', age_fc1, 256, keep_prob)
    y_age_conv = _FC('age_softmax', age_fc2, 101, keep_prob, 'softmax')
    
    return y_smile_conv, y_gender_conv, y_age_conv, phase_train, keep_prob

def load_network():
    sess = tf.Session()
    x = tf.placeholder(tf.float32, [None, 48, 48, 1])
    y_smile_conv, y_gender_conv, y_age_conv, phase_train, keep_prob = BKNetModel(x)
    saver = tf.train.Saver()
    saver.restore(sess, '/opt/data/face/model-age101.ckpt')
    return sess, x, y_smile_conv, y_gender_conv, y_age_conv, phase_train, keep_prob

def draw_label(image, x, y, w, h, label, font=cv2.FONT_HERSHEY_SIMPLEX, 
               font_scale=1, thickness=2):
    color = (0, 255, 0)
    cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
    cv2.putText(image, label, (x, y - 10), font, font_scale, color, thickness)

def predict_face(img_path):
    # 加载图像
    img = cv2.imread(img_path)
    if img is None:
        print(f"无法加载图像: {img_path}")
        return
    
    original_img = img.copy()
    results = detector.detect_faces(original_img)
    
    if not results:
        print("未检测到人脸")
        plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()
        return
    
    # 加载预训练模型
    sess, x, y_smile_conv, y_gender_conv, y_age_conv, phase_train, keep_prob = load_network()
    
    for result in results:
        face_position = result['box']
        x_coordinate, y_coordinate, w_coordinate, h_coordinate = face_position
        
        # 确保坐标不越界
        x_coordinate = max(0, x_coordinate)
        y_coordinate = max(0, y_coordinate)
        w_coordinate = min(w_coordinate, original_img.shape[1] - x_coordinate)
        h_coordinate = min(h_coordinate, original_img.shape[0] - y_coordinate)
        
        face_img = original_img[y_coordinate:y_coordinate + h_coordinate, 
                               x_coordinate:x_coordinate + w_coordinate]
        
        if face_img.size == 0:
            continue
            
        # 预处理人脸图像
        gray_face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        resized_face = cv2.resize(gray_face, (48, 48))
        normalized_face = (resized_face - 128) / 255.0
        
        # 准备输入数据
        T = np.zeros([48, 48, 1])
        T[:, :, 0] = normalized_face
        test_img = np.array([T])
        
        # 进行预测
        predict_y_smile_conv = sess.run(y_smile_conv, 
                                      feed_dict={x: test_img, phase_train: False, keep_prob: 1.0})
        predict_y_gender_conv = sess.run(y_gender_conv, 
                                       feed_dict={x: test_img, phase_train: False, keep_prob: 1.0})
        predict_y_age_conv = sess.run(y_age_conv, 
                                    feed_dict={x: test_img, phase_train: False, keep_prob: 1.0})
        
        # 解析预测结果
        smile_label = "-_-" if np.argmax(predict_y_smile_conv) == 0 else ":)"
        gender_label = "Female" if np.argmax(predict_y_gender_conv) == 0 else "Male"
        age_label = str(np.argmax(predict_y_age_conv))
        
        label = f"{smile_label}, {gender_label}, {age_label}"
        
        # 绘制检测框和标签
        draw_label(original_img, x_coordinate, y_coordinate, w_coordinate, h_coordinate, label)
        
        # 绘制关键点
        keypoints = result['keypoints']
        color = (0, 255, 0)
        for point_name, point in keypoints.items():
            cv2.circle(original_img, point, 2, color, 2)
    
    # 显示结果
    plt.figure(figsize=(10, 8))
    plt.imshow(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title('人脸分析结果')
    plt.show()
    
    sess.close()

# 主程序
if __name__ == "__main__":
    # 测试图像路径
    test_images = [
        "/opt/data/face/ivan.jpg",
        "/opt/data/face/zhoudongyu.jpg", 
        "/opt/data/face/multi-face.jpg"
    ]
    
    for img_path in test_images:
        print(f"处理图像: {img_path}")
        predict_face(img_path)