import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# 参数设置
n = 58  # 商品数
m = 6  # 供应商数

# 假设的数据
a = np.random.rand(n)  # ai 值随机生成
c = np.random.uniform(10, 20, n)  # 进货成本
d = np.random.uniform(80, 120, n)  # 需求量
beta_0 = np.random.uniform(0.5, 1.5, n)  # beta_i0
beta_1 = np.random.uniform(1.0, 2.0, n)  # beta_i1
G = [np.random.choice(range(n), size=np.random.randint(5, 10), replace=False).tolist() for _ in range(m)]  # 供应商分组

# 适应度和个体定义（最大化问题）
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


# 个体生成函数
def generate_individual():
    x = np.random.randint(0, 2, n).tolist()  # 二进制变量x
    y = np.random.uniform(0, 50, n).tolist()  # 连续变量y
    return creator.Individual(x + y)


# 评估函数
def evaluate(individual):
    x = np.array(individual[:n])
    y = np.array(individual[n:])

    # 计算 z_i
    z = (y - beta_0) / beta_1

    # 目标函数：最大化收益
    profit = np.sum((1 - a) * (z - c) * y)

    # 约束条件
    constraints = [
        27 <= np.sum(x) <= 33,
        np.all(2.5 * x <= y),
        np.all(y <= 50 * x),
        np.all([0.5 * np.sum(d[g]) - np.sum(y[g]) <= 0 for g in G]),
        np.all([np.sum(y[g]) - np.sum(d[g]) <= 0 for g in G]),
        5 - np.sum(x) <= 0,
        5 - np.sum([np.sum(y[g]) for g in G]) <= 0,
    ]
    return profit

# 修复操作，确保变量为实数并在范围内
def repair(individual):
    for i in range(len(individual)):
        if np.iscomplex(individual[i]):
            individual[i] = individual[i].real  # 只取实部
        if i < n:  # 对于 x 变量
            individual[i] = int(round(individual[i]))
            individual[i] = max(0, min(1, individual[i]))
        else:  # 对于 y 变量
            individual[i] = max(0, min(50, individual[i]))
    return individual


# 自定义变异函数
def custom_mutate(individual):
    # 变异之前进行修复，确保个体内没有复数
    repair(individual)
    # 调用多项式有界变异
    tools.mutPolynomialBounded(individual, low=[0] * n + [0] * n, up=[1] * n + [50] * n, eta=20.0, indpb=0.2)
    # 再次修复
    repair(individual)
    return individual,


# 注册遗传算法相关操作
toolbox = base.Toolbox()
toolbox.register("individual", generate_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", custom_mutate)  # 使用自定义变异函数
toolbox.register("select", tools.selTournament, tournsize=3)

# 设置遗传算法参数
population_size = 500
generations = 100
crossover_prob = 0.7
mutation_prob = 0.2

# 初始化种群
population = toolbox.population(n=population_size)

# 记录每一代最优个体的适应度值
best_fitnesses = []


def record_best(population):
    fits = [ind.fitness.values[0] for ind in population]
    best_fitnesses.append(max(fits))


# 运行遗传算法并记录每一代的最优适应度
for gen in range(generations):
    algorithms.eaSimple(population, toolbox, cxpb=crossover_prob, mutpb=mutation_prob, ngen=1, stats=None,
                        halloffame=None, verbose=False)
    record_best(population)

# 提取结果
best_ind = tools.selBest(population, 1)[0]
print("Best individual:", best_ind)
print("Best fitness:", best_ind.fitness.values[0])

# 提取最优解的 x 和 y
x_opt = best_ind[:n]
y_opt = best_ind[n:]

print("Optimal x:", x_opt)
print("Optimal y:", y_opt)

# 绘制适应度曲线
plt.plot(best_fitnesses)
plt.xlabel("Generation")
plt.ylabel("Best Fitness")
plt.title("Evolution of Best Fitness over Generations")
plt.show()
