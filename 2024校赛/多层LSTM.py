# import numpy as np
#
#
# # Sigmoid 激活函数
# def sigmoid(x):
#     return 1 / (1 + np.exp(-x))
#
#
# # Tanh 激活函数
# def tanh(x):
#     return np.tanh(x)
#
#
# # Softmax 函数（用于分类任务）
# def softmax(x):
#     exp_x = np.exp(x - np.max(x))
#     return exp_x / np.sum(exp_x)
#
#
# # 定义多层 LSTM 模型
# class MultiLayerLSTM:
#     def __init__(self, input_size, hidden_size, num_layers, output_size):
#         self.input_size = input_size
#         self.hidden_size = hidden_size
#         self.num_layers = num_layers
#         self.output_size = output_size
#
#         # 初始化权重和偏置
#         self.W_i = np.random.randn(hidden_size, input_size + hidden_size)
#         self.b_i = np.zeros((hidden_size, 1))
#         self.W_f = np.random.randn(hidden_size, input_size + hidden_size)
#         self.b_f = np.zeros((hidden_size, 1))
#         self.W_o = np.random.randn(hidden_size, input_size + hidden_size)
#         self.b_o = np.zeros((hidden_size, 1))
#         self.W_c = np.random.randn(hidden_size, input_size + hidden_size)
#         self.b_c = np.zeros((hidden_size, 1))
#
#         # 输出层权重和偏置
#         self.W_out = np.random.randn(output_size, hidden_size)
#         self.b_out = np.zeros((output_size, 1))
#
#     # 前向传播
#     def forward(self, x_batch):
#         # 初始化隐藏状态和细胞状态
#         h_prev = [np.zeros((self.hidden_size, 1))] * (self.num_layers)
#         c_prev = [np.zeros((self.hidden_size, 1))] * (self.num_layers)
#
#         # 遍历每个时间步
#         for t in range(x_batch.shape[1]):
#             for l in range(self.num_layers):
#                 # 获取当前时间步的隐藏状态
#                 current_hidden_state = h_prev[l].repeat(x_batch.shape[0], axis=1).T
#
#                 # 合并输入和当前时间步的隐藏状态
#                 input_concat = np.concatenate((current_hidden_state, x_batch[:, t, :]), axis=0)
#
#                 # 输入门
#                 i_t = sigmoid(np.dot(self.W_i, input_concat) + self.b_i)
#                 # 遗忘门
#                 f_t = sigmoid(np.dot(self.W_f, input_concat) + self.b_f)
#                 # 输出门
#                 o_t = sigmoid(np.dot(self.W_o, input_concat) + self.b_o)
#                 # 更新细胞状态
#                 c_tilde = tanh(np.dot(self.W_c, input_concat) + self.b_c)
#                 c_prev[l] = f_t * c_prev[l] + i_t * c_tilde
#                 # 更新隐藏状态
#                 h_prev[l] = o_t * tanh(c_prev[l])
#
#         # 最后一个时间步的隐藏状态作为输出
#         output = h_prev[-1]
#
#         # 输出层
#         y = np.dot(self.W_out, output) + self.b_out
#
#         return y
#
#     # 计算损失
#     def calculate_loss(self, output, target):
#         return np.mean((output - target) ** 2)
#
#     # 反向传播
#     def backward(self, x, output, target, learning_rate):
#         # 初始化梯度
#         dW_i, db_i = np.zeros_like(self.W_i), np.zeros_like(self.b_i)
#         dW_f, db_f = np.zeros_like(self.W_f), np.zeros_like(self.b_f)
#         dW_o, db_o = np.zeros_like(self.W_o), np.zeros_like(self.b_o)
#         dW_c, db_c = np.zeros_like(self.W_c), np.zeros_like(self.b_c)
#         dW_out, db_out = np.zeros_like(self.W_out), np.zeros_like(self.b_out)
#
#         # 初始化误差项
#         dh_next = np.zeros((self.hidden_size, 1))
#         dc_next = np.zeros((self.hidden_size, 1))
#
#         # 反向传播每个时间步
#         for t in reversed(range(x.shape[1])):
#             # 计算输出层误差
#             dy = output - target
#
#             # 计算输出层梯度
#             dW_out += np.dot(dy, output.T)
#             db_out += np.sum(dy, axis=1, keepdims=True)
#
#             # 计算隐藏状态误差
#             dh = np.dot(self.W_out.T, dy) + dh_next
#
#             # 反向传播每个层
#             for l in reversed(range(self.num_layers)):
#                 # 梯度从输出门开始
#                 do = tanh(self.c_prev[l]) * dh
#                 do = sigmoid(self.o_t[l]) * (1 - sigmoid(self.o_t[l])) * do
#
#                 # 梯度从细胞状态开始
#                 dc = self.o_t[l] * dh * (1 - tanh(self.c_prev[l]) ** 2)
#                 dc = dc + dc_next
#                 dc_tilde = self.i_t[l] * dc
#                 dc_tilde = (1 - tanh(self.c_tilde[l]) ** 2) * dc_tilde
#
#                 # 梯度从输入门开始
#                 di = self.c_tilde[l] * dc
#                 di = sigmoid(self.i_t[l]) * (1 - sigmoid(self.i_t[l])) * di
#
#                 # 梯度从遗忘门开始
#                 df = self.c_prev[l] * dc
#                 df = sigmoid(self.f_t[l]) * (1 - sigmoid(self.f_t[l])) * df
#
#                 # 计算输入门、遗忘门、输出门、细胞状态的梯度
#                 dW_i += np.dot(di, input_concat.T)
#                 db_i += np.sum(di, axis=1, keepdims=True)
#                 dW_f += np.dot(df, input_concat.T)
#                 db_f += np.sum(df, axis=1, keepdims=True)
#                 dW_o += np.dot(do, input_concat.T)
#                 db_o += np.sum(do, axis=1, keepdims=True)
#                 dW_c += np.dot(dc_tilde, input_concat.T)
#                 db_c += np.sum(dc_tilde, axis=1, keepdims=True)
#
#                 # 计算上一个时间步的隐藏状态误差
#                 dh_next = np.dot(self.W_i[:, :self.hidden_size].T, di) + np.dot(self.W_f[:, :self.hidden_size].T,
#                                                                                 df) + np.dot(
#                     self.W_o[:, :self.hidden_size].T, do) + np.dot(self.W_c[:, :self.hidden_size].T, dc_tilde)
#                 dc_next = self.f_t[l] * dc
#
#         # 梯度裁剪（可选）
#         for dparam in [dW_i, db_i, dW_f, db_f, dW_o, db_o, dW_c, db_c, dW_out, db_out]:
#             np.clip(dparam, -5, 5, out=dparam)
#
#         # 更新权重和偏置
#         self.W_i -= learning_rate * dW_i
#         self.b_i -= learning_rate * db_i
#         self.W_f -= learning_rate * dW_f
#         self.b_f -= learning_rate * db_f
#         self.W_o -= learning_rate * dW_o
#         self.b_o -= learning_rate * db_o
#         self.W_c -= learning_rate * dW_c
#         self.b_c -= learning_rate * db_c
#         self.W_out -= learning_rate * dW_out
#         self.b_out -= learning_rate * db_out
#
#     # 训练模型
#     def train(self, x, y, learning_rate, num_epochs, batch_size):
#         for epoch in range(num_epochs):
#             for i in range(0, len(x), batch_size):
#                 # 获取当前批次的数据和标签
#                 x_batch = x[i:i + batch_size]
#                 y_batch = y[i:i + batch_size]
#
#                 # 前向传播
#                 output = self.forward(x_batch)
#
#                 # 计算损失
#                 loss = self.calculate_loss(output, y_batch)
#
#                 # 反向传播
#                 self.backward(x_batch, output, y_batch, learning_rate)
#
#             # 打印每个 epoch 的损失
#             print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss:.4f}')
#
#
# # 设置超参数
# input_size = 1
# hidden_size = 64
# num_layers = 3
# output_size = 1
# seq_length = 10
# learning_rate = 0.001
# num_epochs = 10
# batch_size = 32
#
# # 创建模型实例
# model = MultiLayerLSTM(input_size, hidden_size, num_layers, output_size)
#
# # 生成模拟数据
# data = np.random.randn(100, seq_length, input_size).astype(np.float32)
# target = np.random.randn(100, output_size).astype(np.float32)
#
# # 训练模型
# model.train(data, target, learning_rate, num_epochs, batch_size)



# import numpy as np
# import tensorflow as tf
#
# # 定义多层 LSTM 模型
# class MultiLayerLSTM(tf.keras.Model):
#     def __init__(self, hidden_size, num_layers, output_size):
#         super(MultiLayerLSTM, self).__init__()
#         self.hidden_size = hidden_size
#         self.num_layers = num_layers
#
#         # 定义多层 LSTM 层
#         self.lstm_layers = [tf.keras.layers.LSTM(hidden_size, return_sequences=True) for _ in range(num_layers)]
#
#         # 输出层
#         self.dense = tf.keras.layers.Dense(output_size)
#
#     def call(self, x):
#         # 初始状态
#         h = [tf.zeros((x.shape[0], self.hidden_size)) for _ in range(self.num_layers)]
#         c = [tf.zeros((x.shape[0], self.hidden_size)) for _ in range(self.num_layers)]
#
#         # 前向传播
#         for lstm_layer in self.lstm_layers:
#             for l in range(self.num_layers):
#                 x, (h[l], c[l]) = lstm_layer(x, initial_state=[h[l], c[l]])
#
#         # 输出层
#         output = self.dense(x[:, -1, :])
#
#         return output
#
# # 设置超参数
# hidden_size = 64
# num_layers = 3
# output_size = 1
# learning_rate = 0.001
# num_epochs = 10
# batch_size = 32
#
# # 创建模型实例
# model = MultiLayerLSTM(hidden_size, num_layers, output_size)
#
# # 编译模型
# model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate),
#               loss=tf.keras.losses.MeanSquaredError())
#
# # 生成模拟数据
# data = np.random.randn(100, 10, 1).astype(np.float32)
# target = np.random.randn(100, 1).astype(np.float32)
#
# # 训练模型
# model.fit(data, target, epochs=num_epochs, batch_size=batch_size)

import numpy as np
import tensorflow as tf

# 定义多层 LSTM 模型
class MultiLayerLSTM(tf.keras.Model):
    def __init__(self, hidden_size, num_layers, output_size):
        super(MultiLayerLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # 定义多层 LSTM 层
        self.lstm_layers = [tf.keras.layers.LSTM(hidden_size, return_sequences=True) for _ in range(num_layers)]

        # 输出层
        self.dense = tf.keras.layers.Dense(output_size)

    def call(self, x):
        # 前向传播
        for lstm_layer in self.lstm_layers:
            x = lstm_layer(x)
        output = self.dense(x[:, -1, :])  # 只取序列最后一个时间步的输出作为输出

        return output

# 设置超参数
hidden_size = 64
num_layers = 3
output_size = 1
learning_rate = 0.001
num_epochs = 100
batch_size = 32

# 创建模型实例
model = MultiLayerLSTM(hidden_size, num_layers, output_size)

# 编译模型
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate),
              loss=tf.keras.losses.MeanSquaredError())

# 生成模拟数据
data = np.random.randn(100, 10, 1).astype(np.float32)
target = np.random.randn(100, 1).astype(np.float32)

# 训练模型
model.fit(data, target, epochs=num_epochs, batch_size=batch_size)

# 训练模型
history = model.fit(data, target, epochs=num_epochs, batch_size=batch_size)

# 输出训练过程中的损失值
print(history.history['loss'])
