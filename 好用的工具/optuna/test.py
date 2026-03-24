import optuna

# 定义目标函数，此乃寻找最佳武功秘籍之旅
def objective(trial):
    # 从-10到10中选择一个数，如择剑法中的剑气长
    x = trial.suggest_float('x', -10, 10)
    return (x - 2) ** 2  # 此式如同练功，求其最小，即为最佳

# 创建一个研究对象，开始你的武林征途
study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=200)  # 百次试炼，寻最佳

# 展示最佳秘籍
print(f"最佳剑气长在: {study.best_params['x']}")