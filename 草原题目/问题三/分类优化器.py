import optuna
import sklearn.datasets
import sklearn.ensemble
import sklearn.model_selection
import sklearn.svm
import sklearn.neural_network
import xgboost as xgb
import wandb

# 初始化 WandB，确保使用正确的项目和实体
wandb.init(project="my_project")

def objective(trial):
    iris = sklearn.datasets.load_iris()
    x, y = iris.data, iris.target

    classifier_name = trial.suggest_categorical("classifier", ["SVC", "RandomForest", "NeuralNetwork", "XGBoost"])

    if classifier_name == "SVC":
        svc_c = trial.suggest_float("svc_c", 1e-10, 1e10, log=True)
        gamma = trial.suggest_categorical("gamma", ["auto", "scale"])
        kernel = trial.suggest_categorical("kernel", ["linear", "rbf", "poly"])
        classifier_obj = sklearn.svm.SVC(C=svc_c, gamma=gamma, kernel=kernel)

    elif classifier_name == "RandomForest":
        rf_max_depth = trial.suggest_int("rf_max_depth", 2, 32, log=True)
        min_samples_split = trial.suggest_int("rf_min_samples_split", 2, 20)
        min_samples_leaf = trial.suggest_int("rf_min_samples_leaf", 1, 10)
        max_features = trial.suggest_categorical("rf_max_features", ["sqrt", "log2"])
        classifier_obj = sklearn.ensemble.RandomForestClassifier(
            max_depth=rf_max_depth, n_estimators=100, min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf, max_features=max_features
        )

    elif classifier_name == "NeuralNetwork":
        nn_alpha = trial.suggest_float("nn_alpha", 1e-5, 1e-1, log=True)
        hidden_layer_sizes = trial.suggest_categorical("hidden_layer_sizes", [64, 128, 256, 512])
        activation = trial.suggest_categorical("activation", ["relu", "tanh", "logistic"])
        solver = trial.suggest_categorical("solver", ["sgd", "adam", "lbfgs"])
        classifier_obj = sklearn.neural_network.MLPClassifier(
            alpha=nn_alpha, hidden_layer_sizes=hidden_layer_sizes, activation=activation, solver=solver, max_iter=5000
        )

    elif classifier_name == "XGBoost":
            xgb_eta = trial.suggest_float("xgb_eta", 0.01, 0.3, log=True)
            xgb_max_depth = trial.suggest_int("xgb_max_depth", 3, 9, log=True)
            min_child_weight = trial.suggest_float("xgb_min_child_weight", 1e-5, 1e2, log=True)
            subsample = trial.suggest_float("xgb_subsample", 0.5, 1.0)
            colsample_bytree = trial.suggest_float("xgb_colsample_bytree", 0.5, 1.0)
            classifier_obj = xgb.XGBClassifier(
                learning_rate=xgb_eta, max_depth=xgb_max_depth, min_child_weight=min_child_weight,
                subsample=subsample, colsample_bytree=colsample_bytree, objective='multi:softmax', num_class=3
            )

    score = sklearn.model_selection.cross_val_score(classifier_obj, x, y, n_jobs=1, cv=3)
    accuracy = score.mean()

    # 记录准确率到 WandB
    wandb.log({'accuracy': accuracy})

    return accuracy

if __name__ == "__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=10)

    print(study.best_trial)

    # 保存实验结果和模型文件
    wandb.save("model.pkl")

    # 将最佳试验的准确率和参数传递给 WandB 来绘制条形图
    # wandb.plot.bar({"accuracy": accuracy}, {"accuracy": accuracy})

    # 结束 WandB 实验
    wandb.finish()
