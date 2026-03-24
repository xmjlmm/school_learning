from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score

# 加载Iris数据集
iris = load_iris()
X = iris.data
y = iris.target

# 将其转化为二分类问题
y = [1 if y_i == 0 else 0 for y_i in y]

# 将数据集分割为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


# 创建AdaBoost分类器
clf = AdaBoostClassifier(n_estimators=100)

# 训练模型
clf.fit(X_train, y_train)

# 进行预测
y_pred = clf.predict(X_test)

# 计算准确度
acc = accuracy_score(y_test, y_pred)
print("准确率: ", acc)