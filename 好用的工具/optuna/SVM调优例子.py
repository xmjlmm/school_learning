import optuna
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import wandb

# wandb.init(project='optuna-example')
# 加载鸢尾花数据集
iris = datasets.load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2)

# 定义目标函数
def objective(trial):
    # 定义搜索空间
    C = trial.suggest_loguniform('C', 1e-5, 1e5)
    gamma = trial.suggest_loguniform('gamma', 1e-5, 1e5)

    # 训练SVM模型
    clf = SVC(C=C, gamma=gamma)
    clf.fit(X_train, y_train)

    # 评估模型性能
    score = clf.score(X_test, y_test)
    # wandb.log({"score": score})
    return score

# 创建Optuna study
study = optuna.create_study(direction='maximize')

# 运行Optuna搜索
study.optimize(objective, n_trials=100)

# 打印最佳超参数和得分
print('Best hyperparameters: ', study.best_params)
print('Best score: ', study.best_value)
# wandb.finish()