import numpy as np
import matplotlib.pyplot as plt

# 定义目标函数
def objective_function(x, y):
    r = np.sqrt(x ** 2 + y ** 2)
    return np.sin(r) / r + np.exp((np.cos(2 * np.pi * x) + np.cos(2 * np.pi * y)) / 2) - 2.71289

# 粒子群优化算法
def particle_swarm_optimization(N=20, max_iter=300, w=1, c1=1.5, c2=1.5):
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

    for iteration in range(max_iter):
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
    return g_best, g_best_value, best_values

def main():
    best_position, best_value, convergence_curve = particle_swarm_optimization()

    print(f"最佳位置: {best_position}, 最大值: {best_value}")

    # 绘制收敛曲线
    plt.plot(convergence_curve)
    plt.title('Convergence Curve')
    plt.xlabel('Iteration')
    plt.ylabel('Best Value')
    plt.grid()
    plt.show()
main()
