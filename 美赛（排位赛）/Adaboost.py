
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
import pandas as pd

file_path = "D://数模//美赛//排位赛//问题一.xlsx"
df = pd.read_excel(file_path)

# 检查和清洗数据
# 删除包含 NaN 的行
df.dropna(inplace=True)

# 选择前10个参数作为自变量，后3个参数作为因变量
X = df.iloc[:, :10]
y = df.iloc[:, 11:]

# 将数据集分割为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


regr = AdaBoostRegressor(n_estimators=100)

# 训练模型
regr.fit(X_train, y_train)

# 进行预测
y_pred = regr.predict(X_test)

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
print("均方误差: ", mse)