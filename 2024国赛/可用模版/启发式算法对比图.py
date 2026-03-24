import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import dual_annealing
from deap import base, creator, tools, algorithms
from pyswarm import pso
from matplotlib.font_manager import FontProperties

# 设置字体
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

# 目标函数
def objective(x):
    f1 = -x[0] ** 2
    f2 = (x[1] - 2) ** 2
    return [f1, f2]

# 遗传算法优化
def genetic_algorithm():
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

    return np.array([ind.fitness.values for ind in population])

# 粒子群优化算法
def particle_swarm_optimization():
    def objective_pso(x):
        f1, f2 = objective(x)
        # Combine multiple objectives into a single scalar value using a weighted sum
        return f1 + f2

    lb = [-10, -10]
    ub = [10, 10]

    xopt, _ = pso(objective_pso, lb, ub, swarmsize=100, maxiter=50, debug=True)
    return np.array([objective(xopt)])

# 模拟退火算法
def simulated_annealing():
    def objective_sa(x):
        f1, f2 = objective(x)
        return f1, f2

    bounds = [(-10, 10), (-10, 10)]
    result = dual_annealing(lambda x: objective_sa(x)[0], bounds, maxiter=50, seed=42)
    return np.array([objective_sa(result.x)])

# NSGA-II优化
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

    return np.array([ind.fitness.values for ind in population])

# 执行优化
ga_results = genetic_algorithm()
pso_results = particle_swarm_optimization()
sa_results = simulated_annealing()
nsga2_results = nsga2_algorithm()

# 绘制结果
plt.figure(figsize=(12, 8))

# 为每个算法绘制折线图
# 注意：我们需要对每种算法的结果按目标函数值进行排序以确保绘制正确的折线图
def sort_by_first_objective(results):
    return results[results[:, 0].argsort()]

ga_results_sorted = sort_by_first_objective(ga_results)
pso_results_sorted = sort_by_first_objective(pso_results)
sa_results_sorted = sort_by_first_objective(sa_results)
nsga2_results_sorted = sort_by_first_objective(nsga2_results)

plt.plot(ga_results_sorted[:, 0], ga_results_sorted[:, 1], 'r-', label='遗传算法 (GA)')
plt.plot(pso_results_sorted[:, 0], pso_results_sorted[:, 1], 'g-', label='粒子群优化 (PSO)')
plt.plot(sa_results_sorted[:, 0], sa_results_sorted[:, 1], 'b-', label='模拟退火 (SA)')
plt.plot(nsga2_results_sorted[:, 0], nsga2_results_sorted[:, 1], 'm-', label='NSGA-II')

plt.xlabel('目标函数1 (f1)', fontproperties=font)
plt.ylabel('目标函数2 (f2)', fontproperties=font)
plt.title('多目标优化算法对比', fontproperties=font)
plt.legend()
plt.grid(True)
plt.show()
