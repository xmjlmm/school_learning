'''
import numpy as np
from scipy.optimize import minimize
import pandas as pd

def loss(value_self, p, sale):
    loss_highest = sale / (0.1 * 0.01)
    value_loss = value_self * p
    return min(value_loss, loss_highest)

def objective_function(x, buy_want, value_self, p):
    sale, buy_not = x
    profit = buy_want * sale * round(buy_not)
    loss_value = loss(value_self, p, profit)
    return profit - loss_value

def optimize_buy_and_sale(buy_want, value_self, p):
    solution = minimize(objective_function, x0=(1000, 0))
    buy_not = solution.x[1]
    sale = round(buy_want * solution.x[0])
    return buy_not, sale

def main():
    buy_want = 1000
    value_self = 100000
    p = 0.01
'''


import random
from deap import base, creator, tools, algorithms
import numpy as np
# 定义损失函数
def loss(value_self, p, sale):
    loss_highest = sale / (0.1 * 0.01)  # 高价值损失
    value_loss = value_self * p  # 期望客户价值损失
    return min(value_loss, loss_highest)

# 定义适应度函数
def evalProfit(individual, value_self, p, buy_want):
    sale, buy_not = individual
    current_loss = loss(value_self, p, sale) * buy_not  # 计算总损失
    get = buy_want * sale * buy_not  # 保险公司的总收入
    profit = get - current_loss  # 净利润

    # 如果总收入大于0，计算赔付率
    if get > 0:
        claim_rate = current_loss / get
        # 赔付率约束：只有当赔付率在60%到80%之间时，解才被认为是可行的
        if not (claim_rate <= 0.8):
            return 0,  # 不满足约束的解适应度为0
    else:
        # 如果总收入不大于0，则不考虑赔付率约束
        return 0,  # 总收入不大于0的解适应度为0

    return profit,  # 返回净利润作为适应度值

# 定义遗传算法的基本结构
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_sale", random.uniform, 100, 1000)
toolbox.register("attr_buy_not", random.choice, [0, 1])  # 修改为只能选择0或1
toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.attr_sale, toolbox.attr_buy_not), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 自定义交叉函数
def customCrossover(ind1, ind2):
    tools.cxBlend(ind1, ind2, alpha=0.5)
    ind1[1], ind2[1] = random.choice([0, 1]), random.choice([0, 1])  # 确保buy_not为0或1
    return ind1, ind2

# 自定义变异函数
def customMutate(individual):
    individual[0] = random.uniform(100, 1000)  # 对sale进行变异
    individual[1] = random.choice([0, 1])  # 保证buy_not只能为0或1
    return individual,

# 参数
value_self = 50000  # 期望客户价值
# 数据收集和优化
data_points = []
p_values = np.arange(0.001, 0.01, 0.0001)
buy_want_values = np.arange(0, 1.0, 0.01)

for p in p_values:# 示例概率值
    for buy_want in buy_want_values:# 示例购买意愿


        toolbox.register("evaluate", evalProfit, value_self=value_self, p=p, buy_want=buy_want)
        toolbox.register("mate", customCrossover)  # 使用自定义的交叉函数
        toolbox.register("mutate", customMutate)  # 使用自定义的变异函数
        toolbox.register("select", tools.selTournament, tournsize=3)

        # 遗传算法参数
        population_size = 100
        crossover_probability = 0.7
        mutation_probability = 0.2
        number_of_generations = 500

        # 创建初始种群
        population = toolbox.population(n=population_size)

        # 运行遗传算法
        final_population = algorithms.eaSimple(population, toolbox, crossover_probability, mutation_probability, number_of_generations, verbose=True)

        # 找出最优个体
        best_ind = tools.selBest(population, 1)[0]
        data_points.append((p, buy_want, best_ind.fitness.values[0]))

        print("Best Individual: ", best_ind)
        print("Best Fitness: ", best_ind.fitness.values[0])

import pandas as pd
import matplotlib.pyplot as plt
# 数据处理和绘图
df = pd.DataFrame(data_points, columns=['P', 'Buy_Want', 'Max_Profit'])
# 保存数据到Excel文件
df.to_excel("D://数模//美赛//正式美赛//op.xlsx", index=False)
print("数据已保存到Excel文件 'optimization_results.xlsx'")


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 数据点
x = df['P']
y = df['Buy_Want']
z = df['Max_Profit']

# 创建3D散点图，使用coolwarm颜色映射，增加点的大小并添加透明度
scatter = ax.scatter(x, y, z, c=z, cmap='coolwarm', marker='o', s=20, alpha=0.6)

# 设置轴标签
ax.set_xlabel('P')
ax.set_ylabel('Buy_Want')
ax.set_zlabel('Max_Profit')

# 添加颜色条
fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5, label='Max Profit')

# 显示图形
plt.show()
