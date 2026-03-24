import numpy as np
import tensorflow as tf
from pyswarm import pso
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd
# 假设的数据预处理函数
def preprocess_data(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:(i + window_size), :])
        y.append(data[i + window_size, -1])
    return np.array(X), np.array(y)


# 定义 LSTM 模型
def create_lstm_model(hidden_layer_size, input_shape):
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(hidden_layer_size, input_shape=input_shape),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# PSO 优化函数
def optimize_lstm(params):
    # 解包参数
    window_size, hidden_layer_size = params

    # 数据预处理
    X, y = preprocess_data(data, int(window_size))

    # 分割数据集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 创建 LSTM 模型
    model = create_lstm_model(int(hidden_layer_size), input_shape=X_train.shape[1:])

    # 训练模型
    model.fit(X_train, y_train, epochs=30, batch_size=3200, verbose=0)

    # 在测试集上评估模型
    loss = model.evaluate(X_test, y_test, verbose=0)

    return loss

# 加载您的数据
# 读取数据
dataframe = pd.read_excel("D://数模//美赛//提高//mydata.xlsx")
data = dataframe['cnt'].values  # 替换为你的列名

# 数据归一化
scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data.reshape(-1, 1))

# PSO 参数
lb = [1, 1]  # 参数的下界（窗口大小和隐藏层大小）
ub = [10, 50]  # 参数的上界

# 执行 PSO
xopt, fopt = pso(optimize_lstm, lb, ub, swarmsize=50, maxiter=30, debug=True)

print("最优滑动窗口大小和隐藏层大小:", xopt)
print("在这些参数下的最小损失:", fopt)