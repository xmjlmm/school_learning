'''
import cvxpy as cp
import numpy as np

# 定义变量
c_b = cp.Variable()
c_m = cp.Variable()
c_p = cp.Variable()
r = cp.Parameter()
w = cp.Parameter()

# 定义目标函数
obj = c_b + c_m + c_p

# 定义约束条件
constraints = [
    0.6 <= r / (w - c_p) <= 0.8,
    0 <= w <= 1,
    c_p < c_b * w
]

# 创建问题
problem = cp.Problem(cp.Minimize(obj), constraints)

# 设置参数值
r.value = np.random.uniform(0.6, 0.8)
w.value = np.random.uniform(0, 1)
c_b.value = np.random.uniform(1, 10)
c_m.value = np.random.uniform(1, 10)

# 求解问题
problem.solve()

# 输出结果
print("建筑成本:", c_b.value)
print("维护成本:", c_m.value)
print("保费金额:", c_p.value)
print("风险评估值:", r.value)
print("购买意愿:", w.value)
print(" solved with status:", problem.status)
'''

'''
import numpy as np
from collections import deque
import random
import matplotlib.pyplot as plt

def genetic_algorithm(f, bounds, n_iter, pop_size, elite_size, mutation_rate):
    def generate_population(bounds, pop_size):
        population = []
        for _ in range(pop_size):
            individual = [random.uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]
            population.append(individual)
        return population

    def crossover(parent1, parent2):
        child1, child2 = [], []
        for i in range(len(parent1)):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        return child1, child2

    def mutate(individual, bounds, mutation_rate):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                individual[i] = random.uniform(bounds[i][0], bounds[i][1])
        return individual

    def selection(population, fitness_values, elite_size):
        sorted_indices = np.argsort(fitness_values)
        sorted_population = [population[i] for i in sorted_indices]
        return sorted_population[:elite_size]

    population = generate_population(bounds, pop_size)
    fitness_values = [f(*individual) for individual in population]

    for _ in range(n_iter):
        new_population = []
        for _ in range(pop_size // 2):
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1, bounds, mutation_rate)
            child2 = mutate(child2, bounds, mutation_rate)
            new_population.append(child1)
            new_population.append(child2)

        new_population = selection(new_population, fitness_values, elite_size)
        population = new_population
        fitness_values = [f(*individual) for individual in population]

    best_individual = population[0]
    return best_individual

def f(x, y):
    # 这里是一个简单的目标函数，你可以根据实际问题进行修改
    return x + y

bounds = [(0, 10), (0, 10)]
n_iter = 100
pop_size = 100
elite_size = 20
mutation_rate = 0.1

result = genetic_algorithm(f, bounds, n_iter, pop_size, elite_size, mutation_rate)
print("Optimal solution:", result)
print("Objective function value:", f(*result))
'''


import random
from deap import base, creator, tools, algorithms
import numpy as np

# 定义问题参数
COST_MAX = 1000  # 建筑在极端天气事件下的最大损失值
R_MIN = 0.5  # 最小恢复能力
LAND_MAX = 10000  # 最大环境承载量

# 定义损失函数
def loss_function(individual):
    input_cost, insurance_gap, policy_cost, resilience_benefit = individual
    total_cost = input_cost + insurance_gap + policy_cost - resilience_benefit
    return total_cost,

# 定义约束条件
def check_constraints(individual):
    input_cost, insurance_gap, policy_cost, resilience_benefit = individual
    resilience = random.uniform(0, 1)  # 假设恢复能力为随机值
    land_use = random.uniform(0, LAND_MAX)  # 假设土地使用为随机值

    if input_cost >= COST_MAX or resilience < R_MIN or land_use >= LAND_MAX:
        return False
    return True

# 设置遗传算法
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0, 1000)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=4)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", loss_function)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)

# 检查约束的装饰器
def feasible(individual):
    return check_constraints(individual)

toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, 7e10))

# 运行遗传算法
population = toolbox.population(n=50)
algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=100, verbose=False)

# 找出最优个体
best_ind = tools.selBest(population, 1)[0]
print("Best individual is %s, with fitness %s" % (best_ind, best_ind.fitness.values))
