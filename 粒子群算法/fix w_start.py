import numpy as np
import matplotlib.pyplot as plt


# 定义目标函数
def objective_function(x, y):
    r = np.sqrt(x ** 2 + y ** 2)
    r = np.where(r == 0, 1e-6, r)  # 避免 r 为 0
    return np.sin(r) / r + np.exp((np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)) / 2) - 2.71289


# 粒子群优化算法，带动态权重策略
def particle_swarm_optimization(N=20, max_iter=300, strategy="w-2", w_start=0.9, w_end=0.4, c=0.5, c1=1.5, c2=1.5):
    positions = np.random.uniform(-2, 2, (N, 2))
    velocities = np.random.uniform(-0.5, 0.5, (N, 2))
    p_best = positions.copy()
    p_best_values = np.array([objective_function(x, y) for x, y in positions])
    g_best = p_best[np.argmax(p_best_values)]
    g_best_value = np.max(p_best_values)
    best_values = []

    for k in range(max_iter):
        if strategy == "w-2":
            w = w_start - (w_start - w_end) * (max_iter - k) / max_iter
        elif strategy == "w-3":
            w = w_start - (w_start - w_end) * (k / max_iter) ** 2
        elif strategy == "w-4":
            w = w_start + (w_start - w_end) * (2 * k / max_iter - (k / max_iter) ** 2)
        elif strategy == "w-5":
            w = w_end - (w_start - w_end) / (1 + c * k / max_iter)

        for i in range(N):
            r1, r2 = np.random.rand(), np.random.rand()
            velocities[i] = (w * velocities[i] +
                             c1 * r1 * (p_best[i] - positions[i]) +
                             c2 * r2 * (g_best - positions[i]))
            positions[i] += velocities[i]
            positions[i] = np.clip(positions[i], -2, 2)

            current_value = objective_function(positions[i][0], positions[i][1])
            if current_value > p_best_values[i]:
                p_best[i] = positions[i]
                p_best_values[i] = current_value

        if np.max(p_best_values) > g_best_value:
            g_best_value = np.max(p_best_values)
            g_best = p_best[np.argmax(p_best_values)]

        best_values.append(g_best_value)
    return best_values


# 运行实验，遍历不同的 w_start 和 w_end
def run_experiments_with_weights(max_iter=300, N=20, strategy="w-5", w_start_values=[0.8, 0.9, 1.0],
                                 w_end_values=[0.3, 0.4, 0.5], num_runs=10):
    results = {}

    for w_start in w_start_values:
        for w_end in w_end_values:
            all_convergence_curves = []
            for _ in range(num_runs):
                convergence_curve = particle_swarm_optimization(N=N, max_iter=max_iter, strategy=strategy,
                                                                w_start=w_start, w_end=w_end)
                all_convergence_curves.append(convergence_curve)

            # 计算平均收敛曲线
            avg_convergence_curve = np.mean(all_convergence_curves, axis=0)
            results[(w_start, w_end)] = avg_convergence_curve

    return results


# 绘制不同 (w_start, w_end) 组合的收敛曲线
def main():
    max_iter = 300
    strategy = "w-5"
    w_start_values = [0.8, 0.9, 1.0]
    w_end_values = [0.3, 0.4, 0.5]

    # 运行实验
    results = run_experiments_with_weights(max_iter=max_iter, strategy=strategy, w_start_values=w_start_values,
                                           w_end_values=w_end_values)

    # 绘制收敛曲线
    plt.figure(figsize=(12, 8))
    for (w_start, w_end), avg_convergence_curve in results.items():
        label = f"w_start={w_start}, w_end={w_end}"
        plt.plot(avg_convergence_curve, label=label)

    plt.title(f'Convergence Curves for Different w_start and w_end Combinations ({strategy})')
    plt.xlabel('Iteration')
    plt.ylabel('Best Value')
    plt.legend()
    plt.grid()
    plt.show()


main()
