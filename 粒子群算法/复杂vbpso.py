import numpy as np
import matplotlib.pyplot as plt

# 生成随机的城市坐标
num_cities = 50  # 城市数量
cities = np.random.rand(num_cities, 2) * 100  # 随机生成城市坐标

# 参数设置
population_size = 50  # 粒子群体大小
max_iter = 200  # 最大迭代次数
w = 0.8  # 惯性权重
c1 = 1.5  # 个体学习因子
c2 = 1.5  # 群体学习因子
alpha = 0.5  # 目标1与目标2的权重

# 初始化粒子位置和速度
positions = np.random.rand(population_size, num_cities) * num_cities  # 随机初始化路径（粒子的位置）
velocities = np.random.rand(population_size, num_cities) * 0.1  # 随机初始化速度

# 计算目标函数值
def objective_function(position, cities):
    # 计算路径长度（目标1）
    dist = 0
    for i in range(len(position) - 1):
        dist += np.linalg.norm(cities[int(position[i]) % num_cities] - cities[int(position[i+1]) % num_cities])
    dist += np.linalg.norm(cities[int(position[-1]) % num_cities] - cities[int(position[0]) % num_cities])  # 回到起点

    # 计算传输时间（目标2），假设时间与速度成反比
    speed = 10  # 假设速度为常数
    time = dist / speed  # 传输时间

    obj1 = dist  # 目标函数1：路径长度
    obj2 = time  # 目标函数2：传输时间

    return obj1, obj2

# V型函数替代sigmoid
def v_shaped(x):
    return 1 / (1 + np.abs(x))

# 粒子群优化算法
def bpsop_tsp(cities, population_size=50, max_iter=200, w=0.8, c1=1.5, c2=1.5, alpha=0.5):
    num_cities = len(cities)
    positions = np.random.rand(population_size, num_cities) * num_cities  # 随机初始化路径（粒子的位置）
    velocities = np.random.rand(population_size, num_cities) * 0.1  # 随机初始化速度

    # 初始化个体最佳和全局最佳
    p_best_positions = positions.copy()
    p_best_values = np.full(population_size, np.inf)  # 用一个极大的初始值表示每个粒子的初始目标值
    g_best_position = None
    g_best_value = np.inf

    # 用于记录每次迭代的最佳值
    convergence_curve = []

    for iteration in range(max_iter):
        for i in range(population_size):
            # 计算当前粒子的目标函数值
            obj1, obj2 = objective_function(positions[i], cities)
            combined_obj_value = alpha * obj1 + (1 - alpha) * obj2  # 合并目标函数

            # 更新个体最佳
            if combined_obj_value < p_best_values[i]:
                p_best_positions[i] = positions[i]
                p_best_values[i] = combined_obj_value

            # 更新全局最佳
            if combined_obj_value < g_best_value:
                g_best_position = positions[i]
                g_best_value = combined_obj_value

        # 更新速度和位置
        for i in range(population_size):
            r1 = np.random.rand(num_cities)
            r2 = np.random.rand(num_cities)

            # 更新粒子的速度（使用V型函数）
            velocities[i] = (w * velocities[i] +
                             c1 * r1 * (p_best_positions[i] - positions[i]) +
                             c2 * r2 * (g_best_position - positions[i]))

            # 使用V型函数进行位置更新
            s = v_shaped(velocities[i])  # V型函数代替sigmoid函数
            new_position = np.where(np.random.rand(num_cities) < s, 1, 0)

            # 更新粒子的路径（位置）
            positions[i] = positions[i] + velocities[i]
            positions[i] = np.clip(positions[i], 0, num_cities - 1)  # 保证位置在合理范围内

        # 记录每次迭代的最佳值
        convergence_curve.append(g_best_value)

        # 打印当前迭代的最佳值
        print(f"Iteration {iteration + 1}/{max_iter}, Best Value: {g_best_value}")

    return g_best_position, g_best_value, convergence_curve

# 运行粒子群优化算法
best_position, best_value, convergence_curve = bpsop_tsp(cities, population_size=50, max_iter=200)

# 打印结果
print("Best Solution:", best_position)
print("Best Value (Combined Objective):", best_value)

# 绘制收敛曲线
plt.plot(convergence_curve)
plt.title('Convergence Curve of BPSO for TSP with V-Shaped Function')
plt.xlabel('Iteration')
plt.ylabel('Best Value (Combined Objective)')
plt.grid(True)
plt.show()

# 绘制路径图
best_path = np.argsort(best_position.astype(int))  # 排序得到路径顺序
path_coordinates = cities[best_path]

plt.figure(figsize=(8, 6))
plt.plot(path_coordinates[:, 0], path_coordinates[:, 1], marker='o', linestyle='-', color='b')
plt.scatter(cities[:, 0], cities[:, 1], color='r', marker='x')
for i, txt in enumerate(best_path):
    plt.annotate(txt, (path_coordinates[i, 0], path_coordinates[i, 1]), textcoords="offset points", xytext=(0, 5), ha='center')
plt.title('Best Path Found by BPSO with V-Shaped Function')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.show()
