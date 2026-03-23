import numpy as np
import random
import math
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


# 初始化种群
def initialize_population(pop_size, num_centers):
    return [random.sample(range(len(cities)), num_centers) for _ in range(pop_size)]


# 克隆和变异操作
def clone_and_mutate(individual, mutation_rate=0.5):
    new_individual = individual[:]
    for _ in range(int(len(new_individual) * mutation_rate)):
        new_individual[random.randint(0, len(new_individual) - 1)] = random.randint(0, len(cities) - 1)
    return new_individual


# 主免疫算法
def immune_algorithm(pop_size, num_centers, generations):
    population = initialize_population(pop_size, num_centers)
    best_solution = None
    best_fitness = float('inf')
    fitness_history = []  # 用于记录每代的最佳适应度值

    for gen in range(generations):
        new_population = []

        # 计算适应度并选择优秀个体进行克隆
        for individual in population:
            fit = fitness(individual)
            if fit < best_fitness:
                best_fitness = fit
                best_solution = individual

            # 记录当前代的最佳适应度
            fitness_history.append(best_fitness)

            # 克隆并变异
            new_population.append(clone_and_mutate(individual))

        # 选择最优个体更新种群
        population = sorted(new_population, key=fitness)[:pop_size]

    # 绘制迭代曲线
    plt.plot(fitness_history)
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.title('Immune Algorithm Convergence')
    plt.show()

    # 为每个城市找到对应的中心城市
    city_to_center = {}
    for i in range(len(cities)):
        if i not in best_solution:
            closest_center = min(best_solution, key=lambda center: distance(i, center))
            city_to_center[i] = closest_center
        else:
            city_to_center[i] = i  # 自己是中心城市

    return best_solution, best_fitness, city_to_center


# 运行算法
best_centers, min_cost, city_to_center = immune_algorithm(pop_size=500, num_centers=6, generations=500)
print("最佳中心城市组合:", best_centers)
print("最小加权总距离:", min_cost)
print("每个城市的中心城市选择:")
for city, center in city_to_center.items():
    print(f"城市 {city} 的中心城市是 {center}")
