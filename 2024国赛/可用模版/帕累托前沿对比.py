import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
import pyswarms as ps
from matplotlib.font_manager import FontProperties

# 设置字体
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

# 目标函数
def objective(x):
    f1 = -x[0] ** 2
    f2 = (x[1] - 2) ** 2
    return [f1, f2]

# DEAP 实现的 NSGA-II
def nsga2_algorithm():
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, 1.0))
    creator.create("Individual", list, fitness=creator.FitnessMulti)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", np.random.uniform, -10, 10)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=2)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", objective)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutPolynomialBounded, low=-10, up=10, eta=1.0, indpb=0.2)
    toolbox.register("select", tools.selNSGA2)

    population = toolbox.population(n=100)
    algorithms.eaMuPlusLambda(population, toolbox, mu=100, lambda_=200, cxpb=0.7, mutpb=0.2, ngen=50, verbose=False)

    # 返回所有个体的适应度
    return np.array([ind.fitness.values for ind in population])

# PySwarms 实现的 MOPSO
def particle_swarm_optimization():
    def objective_pso(x):
        return np.array([objective(xi)[0] + objective(xi)[1] for xi in x])

    lb = [-10, -10]
    ub = [10, 10]

    optimizer = ps.single.GlobalBestPSO(n_particles=100, dimensions=2, options={'c1': 0.5, 'c2': 0.3, 'w': 0.9},
                                        bounds=(lb, ub))
    # 进行优化并获取所有粒子的位置
    cost, pos = optimizer.optimize(objective_pso, iters=50)

    # 从每个粒子的位置中获取结果
    results = np.array([objective(p) for p in optimizer.pos_history[-1]])  # 选择最后一代粒子
    return np.unique(results, axis=0)

# 执行优化
nsga2_results = nsga2_algorithm()
pso_results = particle_swarm_optimization()

# 绘制结果
plt.figure(figsize=(12, 8))

# 绘制 NSGA-II 结果
plt.plot(nsga2_results[:, 0], nsga2_results[:, 1], 'r-', label='NSGA-II', marker='o')

# 绘制 MOPSO 结果
plt.plot(pso_results[:, 0], pso_results[:, 1], 'g-', label='MOPSO', marker='x')

plt.xlabel('目标函数1 (f1)', fontproperties=font)
plt.ylabel('目标函数2 (f2)', fontproperties=font)
plt.title('多目标优化算法对比', fontproperties=font)
plt.legend()
plt.grid(True)
plt.show()
