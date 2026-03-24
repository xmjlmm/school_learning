
'''
import tensorflow as tf

tensorflow_version = tf.__version__
gpu_available = tf.test.is_gpu_available()

print('tensorflow version', tensorflow_version, '\tGPU available', gpu_available)

a = tf.constant([1.0,2.0], name = 'a')
b = tf.constant([1.0,2.0], name = 'b')
result = tf.add(a, b, name = 'add')
print(result)

'''

'''
import tensorflow as tf

print(tf.__version__)
print(tf.test.gpu_device_name())
print(tf.config.experimental.set_visible_devices)
print('GPU:', tf.config.list_physical_devices('GPU'))
print('CPU:', tf.config.list_physical_devices(device_type='CPU'))
print(tf.config.list_physical_devices('GPU'))
print(tf.test.is_gpu_available())
# 输出可用的GPU数量
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
# 查询GPU设备
'''