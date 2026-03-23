import numpy as np
import math
import random
import matplotlib.pyplot as plt

cities = np.array([
    [1304, 2312], [3639, 1315], [4177, 2244], [3712, 1399], [3488, 1535],
    [3326, 1556], [3238, 1229], [4196, 1044], [4312, 790], [4386, 570],
    [3007, 1970], [2562, 1756], [2788, 1491], [2381, 1676], [1332, 695],
    [3715, 1678], [3918, 2179], [4061, 2370], [3780, 2212], [3676, 2578],
    [4029, 2838], [4263, 2931], [3429, 1908], [3507, 2376], [3394, 2643],
    [3439, 3201], [2935, 3240], [3140, 3550], [2545, 2357], [2778, 2826],
    [2370, 2975]
])

demands = np.array([20, 90, 90, 60, 70, 70, 40, 90, 90, 70, 60, 40, 40, 20, 80, 80, 90, 70, 100,
                    50, 50, 80, 70, 50, 40, 40, 70, 40, 60, 50, 40, 30])


# 计算两个城市之间的欧几里得距离
def distance(a, b):
    return math.sqrt((cities[a][0] - cities[b][0]) ** 2 + (cities[a][1] - cities[b][1]) ** 2)


# 适应度函数：计算所有非中心城市到最近中心城市的加权最短距离和
def fitness(centers):
    total_cost = 0
    for i in range(len(cities)):
        if i not in centers:
            min_dist = min(distance(i, center) for center in centers)
            if min_dist <= 3000:  # 距离约束
                total_cost += min_dist * demands[i]
            else:
                return float('inf')  # 违反约束返回极大值
    return total_cost


# 粒子类定义
class Particle:
    def __init__(self, num_centers):
        self.position = random.sample(range(len(cities)), num_centers)  # 随机初始化位置
        self.velocity = [0] * num_centers  # 初始化速度
        self.best_position = self.position[:]  # 个体最优位置
        self.best_fitness = fitness(self.position)  # 个体最优适应度


# 粒子群优化算法
def pso_algorithm(pop_size, num_centers, generations, w=0.5, c1=1.5, c2=1.5):
    particles = [Particle(num_centers) for _ in range(pop_size)]
    global_best_position = min(particles, key=lambda p: p.best_fitness).best_position[:]
    global_best_fitness = fitness(global_best_position)
    fitness_history = []  # 记录每代的全局最佳适应度

    for gen in range(generations):
        for particle in particles:
            # 更新粒子的速度和位置
            for i in range(num_centers):
                r1 = random.random()
                r2 = random.random()
                particle.velocity[i] = (w * particle.velocity[i] +
                                        c1 * r1 * (particle.best_position[i] - particle.position[i]) +
                                        c2 * r2 * (global_best_position[i] - particle.position[i]))
                # 更新位置，确保位置为整数且在有效范围内
                particle.position[i] = int(particle.position[i] + particle.velocity[i]) % len(cities)

            # 计算当前适应度
            current_fitness = fitness(particle.position)

            # 更新个体最优
            if current_fitness < particle.best_fitness:
                particle.best_position = particle.position[:]
                particle.best_fitness = current_fitness

            # 更新全局最优
            if current_fitness < global_best_fitness:
                global_best_position = particle.position[:]
                global_best_fitness = current_fitness

        # 记录当前代的全局最佳适应度
        fitness_history.append(global_best_fitness)

    # 绘制迭代曲线
    plt.plot(fitness_history)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.title('PSO Algorithm Convergence')
    plt.show()

    # 为每个城市找到对应的中心城市
    city_to_center = {}
    for i in range(len(cities)):
        if i not in global_best_position:
            closest_center = min(global_best_position, key=lambda center: distance(i, center))
            city_to_center[i] = closest_center
        else:
            city_to_center[i] = i  # 自己是中心城市

    return global_best_position, global_best_fitness, city_to_center


# 运行算法
best_centers, min_cost, city_to_center = pso_algorithm(pop_size=50, num_centers=6, generations=100)
print("最佳中心城市组合:", best_centers)
print("最小加权总距离:", min_cost)
print("每个城市的中心城市选择:")
for city, center in city_to_center.items():
    print(f"城市 {city} 的中心城市是 {center}")
