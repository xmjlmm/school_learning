# 随机森林算法实现分类

# 导入所需的库和数据集
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 加载鸢尾花数据集
iris = load_iris()
X = iris.data  # 特征数据
y = iris.target  # 类别标签
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

# 将数据集分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 创建随机森林分类器对象
# n_estimators 表示森林中树木的数量
# max_depth 表示每棵树的最大深度
rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)

# 在训练集上训练随机森林分类器
rf_classifier.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = rf_classifier.predict(X_test)

# 计算分类器的准确率
accuracy = accuracy_score(y_test, y_pred)
print(f"随机森林分类器在测试集上的准确率：{accuracy:.2f}")

# 获取特征重要性
feature_importances = rf_classifier.feature_importances_
print("特征重要性：")
for i, feature_name in enumerate(iris.feature_names):
    print(f"{feature_name}: {feature_importances[i]:.4f}")

# 绘制特征重要性柱状图
plt.figure(figsize=(8, 6))
plt.bar(range(len(feature_importances)), feature_importances, tick_label=iris.feature_names)
plt.xlabel('特征', font = font)
plt.xticks(rotation=45)
plt.ylabel('重要性', font = font)
plt.title('随机森林特征重要性', font = font)
plt.show()
