import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
from deap import base, creator, tools, algorithms
import random
import pandas as pd

# df = pd.read_excel('')

# 示例参数
C_Trans = np.array([1, 2, 3, 4, 5])  # 假设的运输成本
C_Store = np.array([5, 6])        # 假设的存储成本
V_A = np.array([10, 20])          # A类物料的需求
V_C = np.array([15, 25])          # C类物料的需求


def evaluate(individual):
    # 计算总成本
    trans_cost = sum(C_Trans * individual[:len(C_Trans)])
    store_cost = sum(C_Store * individual[len(C_Trans):])
    total_cost = trans_cost + store_cost
    return total_cost,


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=len(C_Trans) + len(C_Store))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)




population = toolbox.population(n=100)
ngen = 50
cxpb = 0.5
mutpb = 0.2

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("min", np.min)
stats.register("avg", np.mean)

population, logbook = algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen, stats=stats, verbose=True)

min_fitness_values, mean_fitness_values = logbook.select("min", "avg")


plt.plot(min_fitness_values, label='Minimum Fitness')
plt.plot(mean_fitness_values, label='Mean Fitness')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.title('Genetic Algorithm Optimization')
plt.legend()
plt.show()
