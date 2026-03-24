import numpy as np
import random
import matplotlib.pyplot as plt

# Rastrigin函数定义
def rastrigin(individual):
    A = 10
    n = len(individual)
    return A * n + sum([(x ** 2 - A * np.cos(2 * np.pi * x)) for x in individual])

# 初始化种群
def initialize_population(size, dim, bounds):
    population = []
    for _ in range(size):
        individual = [random.uniform(bounds[0], bounds[1]) for _ in range(dim)]
        population.append(individual)
    return population

# 评估种群适应度
def evaluate_population(population):
    fitness_values = []
    for individual in population:
        fitness = rastrigin(individual)
        fitness_values.append(fitness)
    return fitness_values

# 轮盘赌选择
def roulette_wheel_selection(population, fitness_values):
    max_fitness = sum(fitness_values)
    selection_probs = [f / max_fitness for f in fitness_values]
    cumulative_probs = np.cumsum(selection_probs)
    r = random.random()
    for i, individual in enumerate(population):
        if r <= cumulative_probs[i]:
            return individual

# 单点交叉
def crossover(parent1, parent2, crossover_rate):
    if random.random() < crossover_rate:
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1, parent2

# 变异
def mutation(individual, mutation_rate, bounds):
    if random.random() < mutation_rate:
        point = random.randint(0, len(individual) - 1)
        individual[point] = random.uniform(bounds[0], bounds[1])
    return individual

# 克隆
def clone(individual, clone_factor):
    return [individual.copy() for _ in range(clone_factor)]

# 免疫选择
def immune_selection(offspring, fitness_values, suppress_factor):
    selected = []
    for i in range(len(population)):
        if random.random() < suppress_factor:
            selected.append(offspring[i])
    return selected

# 更新免疫记忆池
def update_memory_pool(memory_pool, offspring, fitness_values, memory_pool_size):
    combined = memory_pool + offspring
    combined_fitness = evaluate_population(combined)
    sorted_indices = np.argsort(combined_fitness)
    memory_pool = [combined[i] for i in sorted_indices[:memory_pool_size]]
    return memory_pool

# 更新种群
def update_population(population, offspring, memory_pool, fitness_values):
    combined = population + offspring + memory_pool
    combined_fitness = evaluate_population(combined)
    sorted_indices = np.argsort(combined_fitness)
    new_population = [combined[i] for i in sorted_indices[:len(population)]]
    return new_population

# 判断终止条件
def check_termination_condition(fitness_values, threshold):
    return min(fitness_values) <= threshold

# 获取最优解
def get_best_solution(population, fitness_values):
    best_index = np.argmin(fitness_values)
    return population[best_index]

# 参数设置
population_size = 100     # 种群大小
dim = 10  # 染色体数目
bounds = (-5.12, 5.12)    # 变量的取值范围
max_generations = 1000    # 最大迭代次数
crossover_rate = 0.8      # 交叉概率
mutation_rate = 0.01      # 变异概率
clone_factor = 10         # 克隆数量
suppress_factor = 0.5     # 抑制因子
memory_pool_size = 20     # 记忆池大小
fitness_threshold = 1e-6  # 适应度阈值

# 初始化种群
population = initialize_population(population_size, dim, bounds)

# 评估种群适应度
fitness_values = evaluate_population(population)

# 初始化免疫记忆池
memory_pool = []

# 记录每代的最优适应度值
best_fitness_over_time = []

# 迭代进化过程
for generation in range(max_generations):
    # 选择操作
    parents = [roulette_wheel_selection(population, fitness_values) for _ in range(population_size)]

    # 交叉操作
    offspring = []
    for i in range(0, population_size, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        child1, child2 = crossover(parent1, parent2, crossover_rate)
        offspring.extend([child1, child2])

    # 变异操作
    offspring = [mutation(ind, mutation_rate, bounds) for ind in offspring]

    # 免疫选择
    immune_selected = immune_selection(offspring, fitness_values, suppress_factor)

    # 克隆操作
    cloned_offspring = []
    for ind in immune_selected:
        clones = clone(ind, clone_factor)
        cloned_offspring.extend(clones)

    # 更新免疫记忆池
    memory_pool = update_memory_pool(memory_pool, cloned_offspring, fitness_values, memory_pool_size)

    # 更新种群
    population = update_population(population, cloned_offspring, memory_pool, fitness_values)

    # 评估新的种群适应度
    fitness_values = evaluate_population(population)

    # 记录当前代的最优适应度值
    best_fitness = min(fitness_values)
    best_fitness_over_time.append(best_fitness)

    # 判断终止条件
    if check_termination_condition(fitness_values, fitness_threshold):
        break

# 输出最优解
best_solution = get_best_solution(population, fitness_values)
print("最优解:", best_solution)
print("最优解的适应度值:", rastrigin(best_solution))

# 绘制迭代过程中的最优适应度值变化折线图
plt.plot(best_fitness_over_time)
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.title('Best Fitness over Generations')
plt.show()
