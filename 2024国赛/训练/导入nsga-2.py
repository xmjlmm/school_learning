import numpy as np
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel('')

# 定义多目标问题的权重（最小化问题）
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

# 定义个体生成函数
def generate_individual():
    # 返回每个目标函数的变量个数，这里假设每个目标函数有两个变量，每个变量的范围是0到2
    return creator.Individual([np.random.uniform(0, 2) for _ in range(2)])

# 定义目标函数
# 定义的两个目标函数和两个决策变量
def evaluate(individual):
    x1, x2 = individual
    f1 = x1**2 + x2**2
    f2 = (x1 - 1)**2 + x2**2
    return f1, f2

# 定义约束条件
def feasible(individual):
    x1, x2 = individual
    g1 = x1 + x2 - 1  # 非负性约束
    g2 = x1**2 + x2**2 - 0.5  # 圆形区域约束
    g3 = x1 * x2 - 0.1  # 乘积约束
    return g1 >= 0 and g2 <= 0 and g3 <= 0

# 修复个体，使其满足变量范围和避免复数
def repair(individual):
    for i in range(len(individual)):
        if np.iscomplex(individual[i]):
            individual[i] = individual[i].real
        individual[i] = min(max(individual[i], 0), 2)
    return individual

# 注册遗传算法相关操作
toolbox = base.Toolbox()
# 注册个体生成函数
toolbox.register("individual", generate_individual)
# 注册种群生成函数
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# 注册评估函数
toolbox.register("evaluate", evaluate)
# 注册约束条件检查函数，DeltaPenalty的参数说明：第一个参数表示约束条件是否满足，第二个参数表示惩罚因子
# 为不满足约束的个体施加 100 的惩罚。
# toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, 10.0))  # 惩罚不可行解
# 注册修复个体函数，alpha表示惩罚因子
toolbox.register("mate", tools.cxBlend, alpha=0.5)
# 变异操作，eta表示分布指数，indpb表示个体中元素被变异的概率，low表示变异后个体的下界，up表示变异后个体的上界
# 变异操作，使用多项式分布，变异后个体的值仍需满足变量范围和避免复数
toolbox.register("mutate", tools.mutPolynomialBounded, low=0, up=2, eta=0.1, indpb=0.2)
# 选择操作，使用非支配排序NSGA-II
toolbox.register("select", tools.selNSGA2)
# 映射操作，将评估函数应用于每个个体
toolbox.register("map", map)

# 修复个体的函数调用放在变异和交叉操作之后
def mate_and_repair(ind1, ind2):
    tools.cxBlend(ind1, ind2, alpha=0.5)
    repair(ind1)
    repair(ind2)
    return ind1, ind2

def mutate_and_repair(individual):
    tools.mutPolynomialBounded(individual, low=0, up=2, eta=0.1, indpb=0.2)
    repair(individual)
    return individual,

toolbox.register("mate", mate_and_repair)
toolbox.register("mutate", mutate_and_repair)

# 设置遗传算法参数
population_size = 100
generations = 100
mutation_prob = 0.2
crossover_prob = 0.7

# 初始化种群
population = toolbox.population(n=population_size)

'''
algorithms.eaMuPlusLambda: 执行 µ+λ 遗传算法。
population: 初始种群。
toolbox: 包含遗传算法操作的工具箱。
mu=population_size: 父代个体数量（µ）。
lambda_=population_size: 子代个体数量（λ）。
cxpb=crossover_prob: 交叉概率。
mutpb=mutation_prob: 变异概率。
ngen=generations: 进化代数。
stats=None: 不收集统计数据。
halloffame=None: 不使用名人堂。
verbose=True: 打印进度信息。'''


# # 运行遗传算法
# algorithms.eaMuPlusLambda(population, toolbox, mu=population_size, lambda_=population_size,
#                           cxpb=crossover_prob, mutpb=mutation_prob, ngen=generations,
#                           stats=None, halloffame=None, verbose=True)
#
# # 提取Pareto前沿,Pareto前沿是指在多目标优化问题中，所有目标函数都达到最优解的解集
# pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
#
# # 输出结果
# print("Pareto front:")
# for ind in pareto_front:
#     print(ind, ind.fitness.values)



# 用于记录每一代中的最优适应度值
best_f1 = []
best_f2 = []

# 运行遗传算法并记录每一代的最优适应度值
for gen in range(generations):
    algorithms.eaMuPlusLambda(population, toolbox, mu=population_size, lambda_=population_size,
                              cxpb=crossover_prob, mutpb=mutation_prob, ngen=1,
                              stats=None, halloffame=None, verbose=False)

    # 提取当前种群中两个目标函数的最优值
    fits = [ind.fitness.values for ind in population]
    best_f1.append(min(fit[0] for fit in fits))
    best_f2.append(min(fit[1] for fit in fits))

# 绘制两个目标函数的收敛图
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(best_f1, label="f1: x1^2 + x2^2")
plt.xlabel("Generations")
plt.ylabel("Best f1")
plt.title("Convergence of f1")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(best_f2, label="f2: (x1-1)^2 + x2^2")
plt.xlabel("Generations")
plt.ylabel("Best f2")
plt.title("Convergence of f2")
plt.legend()

plt.tight_layout()
plt.show()

# 提取Pareto前沿
pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]

# 输出结果
print("Pareto front:")
for ind in pareto_front:
    print(ind, ind.fitness.values)

# 绘制Pareto前沿图
plt.figure()
plt.scatter([ind.fitness.values[0] for ind in pareto_front],
            [ind.fitness.values[1] for ind in pareto_front], c="r")
plt.xlabel("f1: x1^2 + x2^2")
plt.ylabel("f2: (x1-1)^2 + x2^2")
plt.title("Pareto Front")
plt.show()
