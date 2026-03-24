'''from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# 加载鸢尾花数据集
iris = datasets.load_iris()
X = iris.data
y = iris.target

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 线性核函数的SVM
clf_linear = svm.SVC(kernel='linear')
clf_linear.fit(X_train, y_train)

# 多项式核函数的SVM
clf_poly = svm.SVC(kernel='poly', degree=3)
clf_poly.fit(X_train, y_train)

# RBF核函数的SVM
clf_rbf = svm.SVC(kernel='rbf')
clf_rbf.fit(X_train, y_train)

# Sigmoid核函数的SVM
clf_sigmoid = svm.SVC(kernel='sigmoid')
clf_sigmoid.fit(X_train, y_train)

# 分别评估四种核函数的模型性能
models = [clf_linear, clf_poly, clf_rbf, clf_sigmoid]
kernel_labels = ['Linear', 'Polynomial', 'RBF', 'Sigmoid']
for clf, kernel in zip(models, kernel_labels):
    y_pred = clf.predict(X_test)
    print(f'Kernel: {kernel}')
    print('Confusion Matrix:')
    print(confusion_matrix(y_test, y_pred))
    print('Classification Report:')
    print(classification_report(y_test, y_pred))
    print()  # 打印空行以分隔不同核函数的结果
'''


# # 导入所需的库
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn import svm, datasets
# from matplotlib.font_manager import FontProperties
#
# # 加载数据集
# iris = datasets.load_iris()
# # 为了简化问题，我们只选择前两种类型的鸢尾花（Setosa和Versicolour），以及两个特征（花瓣长度和花瓣宽度）
# X = iris.data[:100, 2:]
# y = iris.target[:100]
#
# # 创建一个SVM模型实例，这里使用线性核
# model = svm.SVC(kernel='linear')
#
# # 训练模型
# model.fit(X, y)
#
# # 可视化决策边界
# def plot_decision_boundary(model, X, y):
#     # 创建网格来绘制图形
#     x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
#     y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
#     xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
#                          np.arange(y_min, y_max, 0.02))
#
#     # 预测整个网格的分类结果
#     Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
#     Z = Z.reshape(xx.shape)
#
#     # 绘制结果
#     font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=15)
#     plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
#     plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, s=20, edgecolors='k')
#     plt.xlabel('花瓣长度', fontproperties=font)
#     plt.ylabel('花瓣宽度', fontproperties=font)
#     plt.title('SVM的决策边界', fontproperties=font)
#
# plot_decision_boundary(model, X, y)
# plt.show()



import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from matplotlib.font_manager import FontProperties

# 加载数据集
iris = datasets.load_iris()
X = iris.data[:, :2]  # 只取前两个特征，便于可视化
y = iris.target
font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=15)
# 数据集分割为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 创建 SVM 模型
svm_model = SVC(kernel='linear', C=1.0, random_state=42)

# 在训练集上训练模型
svm_model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = svm_model.predict(X_test)

# 计算模型准确率
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# 可视化决策边界
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                     np.arange(y_min, y_max, 0.02))

Z = svm_model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.coolwarm, edgecolors='k')
plt.xlabel('Sepal length', font = font)
plt.ylabel('Sepal width', font = font)
plt.title('SVM Decision Boundary', font = font)
plt.show()





#
#
# import numpy as np
# import pandas as pd
# from sklearn.datasets import load_iris
# import matplotlib.pyplot as plt
# from sklearn.svm import SVC
# from sklearn.model_selection import train_test_split
#
#
# def create_data():
#     iris = load_iris()
#     df = pd.DataFrame(iris.data, columns=iris.feature_names)
#     df['label'] = iris.target
#     df.columns = ['sepal length', 'sepal width', 'petal length', 'petal width', 'label']
#     data = np.array(df.iloc[:100, [0, 1, -1]])
#     for i in range(len(data)):
#         if data[i, -1] == 0:
#             data[i, -1] = -1
#     return data[:, :2], data[:, -1]
#
#
# X, y = create_data()
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
#
# plt.scatter(X[:50, 0], X[:50, 1], label='0')
# plt.scatter(X[50:, 0], X[50:, 1], label='1')
# plt.show()
#
# model = SVC()
# model.fit(X_train, y_train)
#
# SVC(C=1.0, break_ties=False, cache_size=200, class_weight=None, coef0=0.0,
#     decision_function_shape='ovr', degree=3, gamma='scale', kernel='rbf',
#     max_iter=-1, probability=False, random_state=None, shrinking=True,
#     tol=0.001, verbose=False)
#
# print('train accuracy: ' + str(model.score(X_train, y_train)))
# print('test accuracy: ' + str(model.score(X_test, y_test)))