import xgboost as xgb
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
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

# 指定一般的训练参数
params = {
    'objective': 'binary:logistic',
    'eval_metric': 'logloss',
    'use_label_encoder': False,
}

# 为xgboost创建DMatrix
d_train = xgb.DMatrix(X_train, label=y_train)
d_test = xgb.DMatrix(X_test, label=y_test)

# 训练xgboost模型
bst = xgb.train(params, d_train, num_boost_round=100)

# 进行预测
y_pred = bst.predict(d_test)
y_pred = [1 if p > 0.5 else 0 for p in y_pred]

# 计算准确度
acc = accuracy_score(y_test, y_pred)
print("准确率: ", acc)