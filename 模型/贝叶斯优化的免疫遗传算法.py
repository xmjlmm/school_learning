# from skopt import gp_minimize
# from skopt.space import Real, Integer
# from skopt.utils import use_named_args
# import random
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Rastrigin函数定义
# def rastrigin(individual):
#     A = 10
#     n = len(individual)
#     return A * n + sum([(x ** 2 - A * np.cos(2 * np.pi * x)) for x in individual])
#
#
# # 初始化种群
# def initialize_population(size, dim, bounds):
#     population = []
#     for _ in range(size):
#         individual = [random.uniform(bounds[0], bounds[1]) for _ in range(dim)]
#         population.append(individual)
#     return population
#
#
# # 评估种群适应度
# def evaluate_population(population):
#     fitness_values = []
#     for individual in population:
#         fitness = rastrigin(individual)
#         fitness_values.append(fitness)
#     return fitness_values
#
#
# # 轮盘赌选择
# def roulette_wheel_selection(population, fitness_values):
#     max_fitness = sum(fitness_values)
#     selection_probs = [f / max_fitness for f in fitness_values]
#     cumulative_probs = np.cumsum(selection_probs)
#     r = random.random()
#     for i, individual in enumerate(population):
#         if r <= cumulative_probs[i]:
#             return individual
#
#
# # 单点交叉
# def crossover(parent1, parent2, crossover_rate):
#     if random.random() < crossover_rate:
#         point = random.randint(1, len(parent1) - 1)
#         child1 = parent1[:point] + parent2[point:]
#         child2 = parent2[:point] + parent1[point:]
#         return child1, child2
#     return parent1, parent2
#
#
# # 变异
# def mutation(individual, mutation_rate, bounds):
#     if random.random() < mutation_rate:
#         point = random.randint(0, len(individual) - 1)
#         individual[point] = random.uniform(bounds[0], bounds[1])
#     return individual
#
#
# # 克隆
# def clone(individual, clone_factor):
#     return [individual.copy() for _ in range(clone_factor)]
#
#
# # 免疫选择
# def immune_selection(offspring, fitness_values, suppress_factor):
#     selected = []
#     for i in range(len(offspring)):
#         if random.random() < suppress_factor:
#             selected.append(offspring[i])
#     return selected
#
#
# # 更新免疫记忆池
# def update_memory_pool(memory_pool, offspring, fitness_values, memory_pool_size):
#     combined = memory_pool + offspring
#     combined_fitness = evaluate_population(combined)
#     sorted_indices = np.argsort(combined_fitness)
#     memory_pool = [combined[i] for i in sorted_indices[:memory_pool_size]]
#     return memory_pool
#
#
# # 更新种群
# def update_population(population, offspring, memory_pool, fitness_values):
#     combined = population + offspring + memory_pool
#     combined_fitness = evaluate_population(combined)
#     sorted_indices = np.argsort(combined_fitness)
#     new_population = [combined[i] for i in sorted_indices[:len(population)]]
#     return new_population
#
#
# # 判断终止条件
# def check_termination_condition(fitness_values, threshold):
#     return min(fitness_values) <= threshold
#
#
# # 获取最优解
# def get_best_solution(population, fitness_values):
#     best_index = np.argmin(fitness_values)
#     return population[best_index]
#
#
# # 定义目标函数
# @use_named_args(dimensions=[Integer(50, 200, name='population_size'),
#                             Real(0.5, 1.0, name='crossover_rate'),
#                             Real(0.01, 0.1, name='mutation_rate'),
#                             Real(0.1, 1.0, name='suppress_factor')])
# def objective(population_size, crossover_rate, mutation_rate, suppress_factor):
#     population_size = int(population_size)
#     # 初始化种群
#     population = initialize_population(population_size, dim, bounds)
#     # 评估种群适应度
#     fitness_values = evaluate_population(population)
#     # 初始化免疫记忆池
#     memory_pool = []
#     # 记录每代的最优适应度值
#
#     for generation in range(max_generations):
#         parents = [roulette_wheel_selection(population, fitness_values) for _ in range(population_size)]
#
#         # 确保父代个体数量为偶数
#         if len(parents) % 2 != 0:
#             parents.append(parents[random.randint(0, len(parents) - 1)])
#
#         offspring = []
#         for i in range(0, population_size, 2):
#             parent1 = parents[i]
#             parent2 = parents[i + 1]
#             child1, child2 = crossover(parent1, parent2, crossover_rate)
#             offspring.extend([child1, child2])
#         offspring = [mutation(ind, mutation_rate, bounds) for ind in offspring]
#         immune_selected = immune_selection(offspring, fitness_values, suppress_factor)
#         cloned_offspring = []
#         for ind in immune_selected:
#             clones = clone(ind, clone_factor)
#             cloned_offspring.extend(clones)
#         memory_pool = update_memory_pool(memory_pool, cloned_offspring, fitness_values, memory_pool_size)
#         population = update_population(population, cloned_offspring, memory_pool, fitness_values)
#         fitness_values = evaluate_population(population)
#     best_fitness = min(fitness_values)
#     return best_fitness
#
#
# # 参数设置
# dim = 10
# bounds = (-5.12, 5.12)
# max_generations = 100
# clone_factor = 10
# memory_pool_size = 20
# fitness_threshold = 1e-6
#
# # 执行贝叶斯优化
# result = gp_minimize(objective, dimensions=[Integer(50, 200, name='population_size'),
#                                             Real(0.5, 1.0, name='crossover_rate'),
#                                             Real(0.01, 0.1, name='mutation_rate'),
#                                             Real(0.1, 1.0, name='suppress_factor')],
#                      n_calls=50, random_state=0)
#
# # 输出最佳参数组合
# best_params = result.x
# print("最佳参数组合:", best_params)
#
# # 根据最佳参数组合运行IGA
# population_size, crossover_rate, mutation_rate, suppress_factor = best_params
# population = initialize_population(int(population_size), dim, bounds)
# fitness_values = evaluate_population(population)
# memory_pool = []
# for generation in range(max_generations):
#     parents = [roulette_wheel_selection(population, fitness_values) for _ in range(int(population_size))]
#
#     # 确保父代个体数量为偶数
#     if len(parents) % 2 != 0:
#         parents.append(parents[random.randint(0, len(parents) - 1)])
#
#     offspring = []
#     for i in range(0, int(population_size), 2):
#         parent1 = parents[i]
#         parent2 = parents[i + 1]
#         child1, child2 = crossover(parent1, parent2, crossover_rate)
#         offspring.extend([child1, child2])
#     offspring = [mutation(ind, mutation_rate, bounds) for ind in offspring]
#     immune_selected = immune_selection(offspring, fitness_values, suppress_factor)
#     cloned_offspring = []
#     for ind in immune_selected:
#         clones = clone(ind, clone_factor)
#         cloned_offspring.extend(clones)
#     memory_pool = update_memory_pool(memory_pool, cloned_offspring, fitness_values, memory_pool_size)
#     population = update_population(population, cloned_offspring, memory_pool, fitness_values)
#     fitness_values = evaluate_population(population)
#     if check_termination_condition(fitness_values, fitness_threshold):
#         break
# best_solution = get_best_solution(population, fitness_values)
# print("最优解:", best_solution)
# print("最优解的适应度值:", rastrigin(best_solution))
#






from skopt import gp_minimize
from skopt.space import Real, Integer
from skopt.utils import use_named_args
import random
import numpy as np
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
    for i in range(len(offspring)):
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

# 定义目标函数
@use_named_args(dimensions=[Integer(50, 200, name='population_size'),
                            Real(0.5, 1.0, name='crossover_rate'),
                            Real(0.01, 0.1, name='mutation_rate'),
                            Real(0.1, 1.0, name='suppress_factor')])
def objective(population_size, crossover_rate, mutation_rate, suppress_factor):
    population_size = int(population_size)
    # 初始化种群
    population = initialize_population(population_size, dim, bounds)
    # 评估种群适应度
    fitness_values = evaluate_population(population)
    # 初始化免疫记忆池
    memory_pool = []
    best_fitness_per_generation = []

    for generation in range(max_generations):
        parents = [roulette_wheel_selection(population, fitness_values) for _ in range(population_size)]

        # 确保父代个体数量为偶数
        if len(parents) % 2 != 0:
            parents.append(parents[random.randint(0, len(parents) - 1)])

        offspring = []
        for i in range(0, population_size, 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            child1, child2 = crossover(parent1, parent2, crossover_rate)
            offspring.extend([child1, child2])
        offspring = [mutation(ind, mutation_rate, bounds) for ind in offspring]
        immune_selected = immune_selection(offspring, fitness_values, suppress_factor)
        cloned_offspring = []
        for ind in immune_selected:
            clones = clone(ind, clone_factor)
            cloned_offspring.extend(clones)
        memory_pool = update_memory_pool(memory_pool, cloned_offspring, fitness_values, memory_pool_size)
        population = update_population(population, cloned_offspring, memory_pool, fitness_values)
        fitness_values = evaluate_population(population)
        best_fitness_per_generation.append(min(fitness_values))

    best_fitness = min(fitness_values)
    global best_fitness_per_generation_global
    best_fitness_per_generation_global = best_fitness_per_generation
    return best_fitness

# 参数设置
dim = 10
bounds = (-5.12, 5.12)
max_generations = 100
clone_factor = 10
memory_pool_size = 20
fitness_threshold = 1e-6

# 全局变量来记录每代的最优适应度值
best_fitness_per_generation_global = []

# 执行贝叶斯优化
result = gp_minimize(objective, dimensions=[Integer(50, 200, name='population_size'),
                                            Real(0.5, 1.0, name='crossover_rate'),
                                            Real(0.01, 0.1, name='mutation_rate'),
                                            Real(0.1, 1.0, name='suppress_factor')],
                     n_calls=50, random_state=0)

# 输出最佳参数组合
best_params = result.x
print("最佳参数组合:", best_params)

# 根据最佳参数组合运行IGA并记录每代的最优适应度值
population_size, crossover_rate, mutation_rate, suppress_factor = best_params
population = initialize_population(int(population_size), dim, bounds)
fitness_values = evaluate_population(population)
memory_pool = []
best_fitness_per_generation = []

for generation in range(max_generations):
    parents = [roulette_wheel_selection(population, fitness_values) for _ in range(int(population_size))]

    # 确保父代个体数量为偶数
    if len(parents) % 2 != 0:
        parents.append(parents[random.randint(0, len(parents) - 1)])

    offspring = []
    for i in range(0, int(population_size), 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        child1, child2 = crossover(parent1, parent2, crossover_rate)
        offspring.extend([child1, child2])
    offspring = [mutation(ind, mutation_rate, bounds) for ind in offspring]
    immune_selected = immune_selection(offspring, fitness_values, suppress_factor)
    cloned_offspring = []
    for ind in immune_selected:
        clones = clone(ind, clone_factor)
        cloned_offspring.extend(clones)
    memory_pool = update_memory_pool(memory_pool, cloned_offspring, fitness_values, memory_pool_size)
    population = update_population(population, cloned_offspring, memory_pool, fitness_values)
    fitness_values = evaluate_population(population)
    best_fitness_per_generation.append(min(fitness_values))
    if check_termination_condition(fitness_values, fitness_threshold):
        break

best_solution = get_best_solution(population, fitness_values)
print("最优解:", best_solution)
print("最优解的适应度值:", rastrigin(best_solution))

# 绘制免疫遗传算法迭代图
plt.figure(figsize=(10, 5))
plt.plot(best_fitness_per_generation, label='Best Fitness per Generation')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.title('Best Fitness per Generation')
plt.legend()
plt.show()

# 绘制适应度与参数的关系曲线
fitness_values = result.func_vals
params = result.x_iters
params = np.array(params)

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
param_names = ['population_size', 'crossover_rate', 'mutation_rate', 'suppress_factor']

for i, ax in enumerate(axs.flat):
    ax.plot(params[:, i], fitness_values, 'o')
    ax.set_xlabel(param_names[i])
    ax.set_ylabel('Fitness')
    ax.set_title(f'Fitness vs {param_names[i]}')

plt.tight_layout()
plt.show()

