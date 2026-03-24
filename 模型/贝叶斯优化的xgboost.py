import numpy as np
from hyperopt import hp, tpe, fmin, Trials, STATUS_OK
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from hyperopt import space_eval
import xgboost as xgb
import random

# 加载数据集
X, y = load_digits(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 定义XGBoost的超参数空间
space = {
    'max_depth': hp.choice('max_depth', range(1, 21)),
    'learning_rate': hp.uniform('learning_rate', 0.01, 1.0),
    'min_child_weight': hp.choice('min_child_weight', range(1, 11)),
    'subsample': hp.uniform('subsample', 0.1, 1.0),
    'colsample_bytree': hp.uniform('colsample_bytree', 0.1, 1.0),
}

# 定义目标函数
def objective(params):
    model = XGBClassifier(random_state=0, **params)
    best_score = cross_val_score(model, X_train, y_train, scoring='accuracy', cv=5).mean()
    return {'loss': -best_score, 'status': STATUS_OK}

# 运行贝叶斯优化
trials = Trials()
best = fmin(fn=objective,
            space=space,
            algo=tpe.suggest,
            max_evals=50,
            trials=trials)
            # rstate=np.random.RandomState(None)
            # rstate=random.randint(0,2))

# 提取最佳参数
best_params = space_eval(space, best)
print("最优参数:", best_params)

# 使用最优参数训练模型
model = XGBClassifier(random_state=0, **best_params)
model.fit(X_train, y_train)

# 在测试集上评估模型
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("测试集准确率:", accuracy)

from sklearn.metrics import roc_curve, auc, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# 假设best_params包含了贝叶斯优化找到的最佳超参数
# 使用最优参数训练XGBoost模型
model = xgb.XGBClassifier(random_state=0, **best_params)
model.fit(X_train, y_train)

# 预测测试集的概率
y_probs = model.predict_proba(X_test)[:, 1]

# 计算ROC曲线数据
fpr, tpr, _ = roc_curve(y_test, y_probs)
roc_auc = auc(fpr, tpr)

# 绘制ROC曲线
plt.figure()
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()

# 计算混淆矩阵
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)

# 绘制混淆矩阵
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap=plt.cm.Blues)
plt.show()
