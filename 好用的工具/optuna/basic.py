import optuna

# 定义objective要优化的函数，最小化目标函数(x - 2)^2
def objective(trial):
    # 定义超参数的搜索空间，x的空间是-10到10之间的浮点数
    x = trial.suggest_float('x', -10, 10)
    return (x - 2) ** 2

# 创建一个study对象并调用该optimize方法超过 100 次试验
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=1000)
# 输出搜索出的最佳参数
print(study.best_params, 'study.best_value:', study.best_value)
