import numpy as np
import matplotlib.pyplot as plt

# 背包问题参数
volumes = [95, 75, 23, 73, 50, 22, 6, 57, 89, 98]  # 每件物品的体积
values = [89, 59, 19, 43, 100, 72, 44, 16, 7, 64]  # 每件物品的价值
N = len(volumes)  # 物品数量
V = 300  # 背包容量
population_size = 30  # 粒子群数量
max_iter = 100  # 最大迭代次数

# BPSO参数
w = 0.5  # 惯性权重
c1 = 1.5  # 个人学习因子
c2 = 1.5  # 群体学习因子

# 初始化粒子的位置和速度
positions = np.random.randint(2, size=(population_size, N))  # 二进制编码，表示物品是否被选中
velocities = np.random.uniform(-1, 1, (population_size, N))  # 初始速度

# 初始化个体最佳和全局最佳
p_best_positions = positions.copy()
p_best_values = np.zeros(population_size)
for i in range(population_size):
    p_best_values[i] = np.sum(np.array(values) * p_best_positions[i]) if np.sum(
        np.array(volumes) * p_best_positions[i]) <= V else 0

g_best_position = p_best_positions[np.argmax(p_best_values)]
g_best_value = np.max(p_best_values)


# Sigmoid函数
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# 评估函数，计算背包内物品总价值
def evaluate(position):
    total_volume = np.sum(np.array(volumes) * position)
    total_value = np.sum(np.array(values) * position)
    return total_value if total_volume <= V else 0


# 用于记录每次迭代的最佳值
convergence_curve = []

# 粒子群优化过程
for iteration in range(max_iter):
    for i in range(population_size):
        # 更新速度
        r1 = np.random.rand(N)
        r2 = np.random.rand(N)
        velocities[i] = (w * velocities[i] +
                         c1 * r1 * (p_best_positions[i] - positions[i]) +
                         c2 * r2 * (g_best_position - positions[i]))

        # 更新位置
        s = sigmoid(velocities[i])
        new_position = np.where(np.random.rand(N) < s, 1, 0)

        # 评估新的位置
        new_value = evaluate(new_position)

        # 更新个体最佳
        if new_value > p_best_values[i]:
            p_best_positions[i] = new_position
            p_best_values[i] = new_value

        # 更新全局最佳
        if new_value > g_best_value:
            g_best_position = new_position
            g_best_value = new_value

    # 记录每次迭代的全局最佳值
    convergence_curve.append(g_best_value)
    print(f"Iteration {iteration + 1}/{max_iter}, Best Value: {g_best_value}")

# 输出最终结果
print("Best Solution:", g_best_position)
print("Maximum Value:", g_best_value)
print("Total Volume:", np.sum(np.array(volumes) * g_best_position))

# 绘制迭代曲线
plt.figure(figsize=(10, 6))
plt.plot(convergence_curve, label='Best Value')
plt.xlabel('Iteration')
plt.ylabel('Best Value')
plt.title('Convergence Curve of BPSO for Knapsack Problem')
plt.legend()
plt.grid()
plt.show()
