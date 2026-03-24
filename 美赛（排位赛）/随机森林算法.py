import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# 加载数据
file_path = "D://数模//美赛//排位赛//问题一.xlsx"  # 更换为您的文件路径
df = pd.read_excel(file_path)

# 检查和清洗数据
# 删除包含 NaN 的行
df.dropna(inplace=True)

# 选择前10个参数作为自变量，后3个参数作为因变量
X = df.iloc[:, :10]
y = df.iloc[:, 10:]

# 划分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建随机森林回归模型
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

# 训练模型
rf_model.fit(X_train, y_train)

# 预测测试集
y_pred = rf_model.predict(X_test)

# 评估模型
mse = mean_squared_error(y_test, y_pred)
print(f'均方误差(MSE): {mse}')

