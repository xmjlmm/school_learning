# 导入所需的库和数据集
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 加载加州房价数据集
california_housing = fetch_california_housing()
X = california_housing.data  # 特征数据
y = california_housing.target  # 目标房价
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

# 将数据集分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 创建随机森林回归器对象
# n_estimators 表示森林中树木的数量
# max_depth 表示每棵树的最大深度
rf_regressor = RandomForestRegressor(n_estimators=100, max_depth=None, random_state=42)

# 在训练集上训练随机森林回归器
rf_regressor.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = rf_regressor.predict(X_test)

# 计算回归器的均方误差（MSE）
mse = mean_squared_error(y_test, y_pred)
print(f"随机森林回归器在测试集上的均方误差：{mse:.2f}")

# 获取特征重要性
feature_importances = rf_regressor.feature_importances_
print("特征重要性：")
for i, feature_name in enumerate(california_housing.feature_names):
    print(f"{feature_name}: {feature_importances[i]:.4f}")

# 绘制特征重要性柱状图
plt.figure(figsize=(8, 6))
plt.bar(california_housing.feature_names, feature_importances)
plt.xlabel('特征', font = font, fontsize=12)
plt.ylabel('重要性', font = font, fontsize=12)
plt.title('随机森林特征重要性', font = font, fontsize=14)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
