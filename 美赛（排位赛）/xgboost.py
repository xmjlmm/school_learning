import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

file_path = "D://数模//美赛//排位赛//问题一.xlsx"  # 更换为您的文件路径
df = pd.read_excel(file_path)

# 检查并清洗数据,删除包含 NaN 的行
df.dropna(inplace=True)

# 选择前10个参数作为自变量，以最后一个参数作为因变量(y值)
X = df.iloc[:, :10]
y = df.iloc[:, -1]

# 将数据集分割为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 指定通用训练参数
params = {
    'objective': 'reg:squarederror',
    'eval_metric': 'rmse',
    'use_label_encoder': False,
}

# 为xgboost创建DMatrix
d_train = xgb.DMatrix(X_train, label=y_train)
d_test = xgb.DMatrix(X_test, label=y_test)

# 使用xgboost训练模型
bst = xgb.train(params, d_train, num_boost_round=100)

# 使用模型进行预测
y_pred = bst.predict(d_test)

# 计算均方差误差
mse = mean_squared_error(y_test, y_pred)
print("均方差误差: ", np.sqrt(mse))