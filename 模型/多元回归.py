import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm

# 生成随机数据
np.random.seed(42)
n_samples = 100
n_features = 3

# 生成自变量数据
X = np.random.rand(n_samples, n_features)

# 生成目标变量数据，添加一些噪声
coefficients = np.array([2, -1, 3])
y = X.dot(coefficients) + np.random.randn(n_samples)

# 将数据分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 训练线性回归模型
model = LinearRegression()
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 计算MSE和R^2
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# 显示MSE和R^2
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"R^2: {r2:.2f}")

# 进行显著性检验
# 使用statsmodels来获取回归统计信息
X_train_sm = sm.add_constant(X_train)  # 添加常数项
model_sm = sm.OLS(y_train, X_train_sm).fit()

# 显示回归结果
print(model_sm.summary())
