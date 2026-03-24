import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from skopt import BayesSearchCV
from skopt.space import Real, Integer

# 生成数据集，调整类别的簇数量为1
X, y = make_classification(n_samples=1000, n_features=20, n_informative=2, n_redundant=10, n_classes=3, n_clusters_per_class=1, weights=[0.2, 0.3, 0.5])
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 数据标准化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 定义分类器
rf = RandomForestClassifier(class_weight='balanced')
xgb = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
svm = SVC(probability=True, class_weight='balanced')
mlp = MLPClassifier(max_iter=300, activation='relu', solver='adam', random_state=1)

# 贝叶斯优化参数
search_spaces = {
    'n_estimators': Integer(10, 300),
    'max_depth': Integer(3, 10)
}

opt = BayesSearchCV(rf, search_spaces, n_iter=100, cv=3, n_jobs=-1)
opt.fit(X_train, y_train)

print("最优参数: ", opt.best_params_)
print("最佳得分: ", opt.best_score_)

# 更新随机森林分类器的参数
rf.set_params(**opt.best_params_)

# 软投票分类器
voting_clf = VotingClassifier(
    estimators=[('rf', rf), ('xgb', xgb), ('svm', svm), ('mlp', mlp)],
    voting='soft'
)
voting_clf.fit(X_train, y_train)

# 预测并计算准确率
y_pred = voting_clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'准确率: {accuracy}')

