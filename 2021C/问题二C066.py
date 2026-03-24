import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from matplotlib.font_manager import FontProperties

# 设置中文字体
font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc", size=14)

# 定义问题的参数
num_items = 3  # 例如三种商品 A, B, C
num_periods = 1  # 例如一个时段
C_Transport = np.array([10, 15, 20])  # 每种商品的运输成本
C_Purchase = np.array([12, 11, 13])  # 每种商品的采购成本
C_Store = np.array([5, 6, 7])  # 每种商品的存储成本

# 定义个体和种群
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0, 100)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=num_items)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# 定义适应度函数
def evaluate(individual):
    x = np.array(individual)
    transport_cost = np.dot(C_Transport, x)
    purchase_cost = np.dot(C_Purchase, x)
    store_cost = np.dot(C_Store, x)

    # 计算总成本
    total_cost = transport_cost + purchase_cost + store_cost

    # 添加约束条件
    constraints_penalty = 0
    # 示例：简单的库存约束
    if np.sum(x) > 100:  # 假设库存不能超过100
        constraints_penalty += 10000  # 添加一个大的惩罚

    return total_cost + constraints_penalty,


toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate)

# 运行遗传算法并记录每一代的最优解
num_generations = 40
population = toolbox.population(n=50)
halloffame = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values if ind.fitness.valid else [float('inf')])
stats.register("min", np.min)

logbook = tools.Logbook()
logbook.record(gen=0, **stats.compile(population))

for gen in range(1, num_generations + 1):
    offspring = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, offspring))

    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.5:
            toolbox.mate(child1, child2)
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:
        if random.random() < 0.2:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # 如果所有个体都无效，用上一代的种群代替
    if len(invalid_ind) == len(offspring):
        offspring = population
    else:
        population[:] = offspring

    halloffame.update(population)
    record = stats.compile(population)
    logbook.record(gen=gen, **record)

# 获取最佳解并打印
best_ind = tools.selBest(population, 1)[0]
print('最优解:', best_ind)
print('最小成本:', evaluate(best_ind)[0])

# 绘制遗传算法的迭代图
min_fitness_values = logbook.select("min")

plt.figure(figsize=(10, 6))
plt.plot(min_fitness_values, label="best")
plt.xlabel("迭代代数", font = font)
plt.ylabel("最优适应度值（成本）", font = font)
plt.title("遗传算法的适应度变化", font = font)
plt.legend()
plt.grid(True)
plt.show()
