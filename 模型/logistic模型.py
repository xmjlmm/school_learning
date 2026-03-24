from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# 示例数据集
features = np.array([[2, 3], [3, 5], [5, 8], [7, 10], [4, 5], [6, 9], [8, 10]])
target = np.array([0, 0, 1, 1, 0, 1, 1])

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# 创建逻辑回归模型
model = LogisticRegression()

# 训练模型
model.fit(X_train, y_train)

# 预测
predictions = model.predict(X_test)

# 评估模型
print("分类报告:")
print(classification_report(y_test, predictions))
print("混淆矩阵:")
print(confusion_matrix(y_test, predictions))
