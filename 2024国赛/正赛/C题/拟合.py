import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"C:\Windows\Fonts\msyh.ttc", size=14)

df = pd.read_excel("F:\\数模\\2024年国赛复习资料\\正式国赛\\赛题\\C题\\备用拟合.xlsx")

max_value = df['销售单价_最大值']
min_value = df['销售单价_最小值']
sea = df['季节']
env = df['地块']
yi = df['亩产量斤']
cos = df['种植成本元亩']

X = [sea, env, yi, cos]
X = df[['季节', '地块', '亩产量斤', '种植成本元亩']]
y_min = df['销售单价_最小值']  # 因变量1：销售单价_最小值
y_max = df['销售单价_最大值']  # 因变量2：销售单价_最大值

# 检查数据维度是否匹配
print(X.shape)  # 应该显示 (样本数量, 4)
print(y_min.shape)  # 应该显示 (样本数量,)
print(y_max.shape)  # 应该显示 (样本数量,)

# 创建二次和三次特征
poly_2 = PolynomialFeatures(degree=2)
poly_3 = PolynomialFeatures(degree=3)

# 二次特征转换
X_poly_2 = poly_2.fit_transform(X)
# 三次特征转换
X_poly_3 = poly_3.fit_transform(X)

# 构建回归模型
model_2_min = LinearRegression()
model_2_max = LinearRegression()
model_3_min = LinearRegression()
model_3_max = LinearRegression()

# 拟合二次模型
model_2_min.fit(X_poly_2, y_min)
model_2_max.fit(X_poly_2, y_max)

# 拟合三次模型
model_3_min.fit(X_poly_3, y_min)
model_3_max.fit(X_poly_3, y_max)

# 进行预测
y_pred_2_min = model_2_min.predict(X_poly_2)
y_pred_2_max = model_2_max.predict(X_poly_2)

y_pred_3_min = model_3_min.predict(X_poly_3)
y_pred_3_max = model_3_max.predict(X_poly_3)

# 计算误差
mse_2_min = mean_squared_error(y_min, y_pred_2_min)
mse_2_max = mean_squared_error(y_max, y_pred_2_max)
mse_3_min = mean_squared_error(y_min, y_pred_3_min)
mse_3_max = mean_squared_error(y_max, y_pred_3_max)

print(f"二次拟合误差 - 最小单价: {mse_2_min}")
print(f"二次拟合误差 - 最大单价: {mse_2_max}")
print(f"三次拟合误差 - 最小单价: {mse_3_min}")
print(f"三次拟合误差 - 最大单价: {mse_3_max}")

# 绘制回归结果对比图
plt.figure(figsize=(14, 6))

# 最小单价对比
plt.subplot(1, 2, 1)
plt.scatter(range(len(y_min)), y_min, color='blue', label='真实值（最小单价）', alpha=0.6)
plt.plot(range(len(y_min)), y_pred_2_min, color='orange', label='二次拟合', linestyle='--')
plt.plot(range(len(y_min)), y_pred_3_min, color='red', label='三次拟合', linestyle='-')
plt.title('最小单价：真实值 vs 二次和三次拟合', font = font)
plt.xlabel('样本点', font = font)
plt.ylabel('销售单价_最小值', font = font)
plt.legend()

# 最大单价对比
plt.subplot(1, 2, 2)
plt.scatter(range(len(y_max)), y_max, color='green', label='真实值（最大单价）', alpha=0.6)
plt.plot(range(len(y_max)), y_pred_2_max, color='orange', label='二次拟合', linestyle='--')
plt.plot(range(len(y_max)), y_pred_3_max, color='red', label='三次拟合', linestyle='-')
plt.title('最大单价：真实值 vs 二次和三次拟合', font = font)
plt.xlabel('样本点', font = font)
plt.ylabel('销售单价_最大值', font = font)
plt.legend()

# 显示图形
plt.tight_layout()
plt.show()