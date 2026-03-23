import numpy as np
import matplotlib.pyplot as plt

# 定义目标函数
def objective_function(x, y):
    r = np.sqrt(x ** 2 + y ** 2)
    return np.sin(r) / r + np.exp((np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)) / 2) - 2.71289

# 不同惯性权重策略的粒子群优化算法
def particle_swarm_optimization(N=20, max_iter=300, strategy="w-2", w_start=0.9, w_end=0.4, c=0.5, c1=1.5, c2=1.5):
    # 初始化粒子位置和速度
    positions = np.random.uniform(-2, 2, (N, 2))
    velocities = np.random.uniform(-0.5, 0.5, (N, 2))

    # 初始化个体最佳位置和全局最佳位置
    p_best = positions.copy()
    p_best_values = np.array([objective_function(x, y) for x, y in positions])
    g_best = p_best[np.argmax(p_best_values)]  # 全局最佳位置
    g_best_value = np.max(p_best_values)

    # 收敛曲线记录
    best_values = []

    for k in range(max_iter):
        # 根据不同策略计算动态权重
        if strategy == "w-1":
            w = w_start
        elif strategy == "w-2":
            w = w_start - (w_start - w_end) * (max_iter - k) / max_iter
        elif strategy == "w-3":
            w = w_start - (w_start - w_end) * (k / max_iter) ** 2
        elif strategy == "w-4":
            w = w_start + (w_start - w_end) * (2 * k / max_iter - (k / max_iter) ** 2)
        elif strategy == "w-5":
            w = w_end - (w_start - w_end) / (1 + c * k / max_iter)

        # 更新粒子速度和位置
        for i in range(N):
            r1 = np.random.rand()
            r2 = np.random.rand()
            velocities[i] = (w * velocities[i] +
                             c1 * r1 * (p_best[i] - positions[i]) +
                             c2 * r2 * (g_best - positions[i]))
            # 边界条件处理
            positions[i] += velocities[i]
            positions[i] = np.clip(positions[i], -2, 2)

            # 更新个体最佳位置
            current_value = objective_function(positions[i][0], positions[i][1])
            if current_value > p_best_values[i]:
                p_best[i] = positions[i]
                p_best_values[i] = current_value

        # 更新全局最佳位置
        if np.max(p_best_values) > g_best_value:
            g_best_value = np.max(p_best_values)
            g_best = p_best[np.argmax(p_best_values)]

        # 记录最佳值
        best_values.append(g_best_value)
    return best_values

def run_experiments(strategy, max_iter=300, N=20, num_runs=10):
    # 多次实验，计算平均收敛曲线
    all_convergence_curves = []
    for _ in range(num_runs):
        convergence_curve = particle_swarm_optimization(N=N, max_iter=max_iter, strategy=strategy)
        all_convergence_curves.append(convergence_curve)

    # 计算平均收敛曲线
    avg_convergence_curve = np.mean(all_convergence_curves, axis=0)
    return avg_convergence_curve

def main():
    max_iter = 300
    strategies = ["w-1", "w-2", "w-3", "w-4", "w-5"]

    # 绘制收敛曲线
    plt.figure(figsize=(10, 6))
    for strategy in strategies:
        avg_convergence_curve = run_experiments(strategy, max_iter=max_iter)
        plt.plot(avg_convergence_curve, label=strategy)

    plt.title('Convergence Curves with Different Inertia Weight Strategies')
    plt.xlabel('Iteration')
    plt.ylabel('Best Value')
    plt.legend()
    plt.grid()
    plt.show()

main()
