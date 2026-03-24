from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.datasets import load_iris, fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

# 示例：分类问题（以鸢尾花数据集为例）
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3, random_state=42)

# 初始化随机森林分类器
clf = RandomForestClassifier(n_estimators=100, max_features='sqrt', random_state=42)

# 训练模型
clf.fit(X_train, y_train)

# 预测
y_pred = clf.predict(X_test)

# 评估模型
print("分类准确率:", accuracy_score(y_test, y_pred))



# 示例：回归问题（以波士顿房价数据集为例）
fetch_california_housing = fetch_california_housing()
X_train, X_test, y_train, y_test = train_test_split(fetch_california_housing.data, fetch_california_housing.target, test_size=0.3, random_state=42)

# 初始化随机森林回归器
reg = RandomForestRegressor(n_estimators=100, max_features='sqrt', random_state=42)

# 训练模型
reg.fit(X_train, y_train)

# 预测
y_pred = reg.predict(X_test)

# 评估模型
print("均方误差:", mean_squared_error(y_test, y_pred))
