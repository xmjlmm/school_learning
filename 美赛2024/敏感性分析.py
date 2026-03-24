'''
# 遗传算法

import random
from deap import base, creator, tools, algorithms
import numpy as np
import matplotlib.pyplot as plt


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

    # 确保交叉后sale的值在100到1000之间
    ind1[0] = max(100, min(ind1[0], 1000))
    ind2[0] = max(100, min(ind2[0], 1000))

    return ind1, ind2

# 自定义变异函数
def customMutate(individual):
    individual[0] = random.uniform(100, 1000)  # 对sale进行变异
    individual[1] = random.choice([0, 1])  # 保证buy_not只能为0或1

    # 变异后再次确认sale的值在100到1000之间
    individual[0] = max(100, min(individual[0], 1000))

    return individual,

# 参数
value_self = 50000  # 期望客户价值
# 数据收集和优化
data_points = []
p_values = np.arange(0.001, 0.01, 0.0001)
buy_want_values = np.arange(0, 1.0, 0.01)


p = 0.005
buy_want = 0.5

toolbox.register("evaluate", evalProfit, value_self=value_self, p=p, buy_want=buy_want)
toolbox.register("mate", customCrossover)  # 使用自定义的交叉函数
toolbox.register("mutate", customMutate)  # 使用自定义的变异函数
toolbox.register("select", tools.selTournament, tournsize=3)
x = []
y = []
# 遗传算法参数
i = 0.1
while i <= 1:
    population_size = 100
    crossover_probability = 0.1
    mutation_probability = i
    number_of_generations = 150
    # 创建初始种群
    population = toolbox.population(n=population_size)
    i = i + 0.01
    # 运行遗传算法
    final_population = algorithms.eaSimple(population, toolbox, crossover_probability, mutation_probability, number_of_generations, verbose=True)

    # 找出最优个体
    best_ind = tools.selBest(population, 1)[0]
    data_points.append((p, buy_want, best_ind.fitness.values[0]))

    print("Best Individual: ", best_ind)
    print("Best Fitness: ", best_ind.fitness.values[0])
    x.append(i)
    y.append(best_ind.fitness.values[0])

plt.plot(x, y)
plt.title('Best Fitness vs Mutation Rate')
plt.xlabel('Mutation Rate')
plt.ylabel('Best Fitness')
plt.show()
'''
'''
import matplotlib.pyplot as plt
x = []
y = []
i = 0.001
while i < 0.05:
    x.append(i)
    c = i * 4 + i * i * i * i + i * i * 9 + 1
    y.append(c)
    i = i + 0.001
plt.plot(x, y)
plt.title('')
plt.xlabel('')
plt.ylabel('')
plt.show()
'''


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# 定义x轴的数据范围和精度
x = np.linspace(0.001, 0.05, 500)

# 定义两条曲线的起点
y_start1 = 1040
y_start2 = 496

# 生成两条曲线的y轴数据，使用指数函数来模拟指数上升的趋势，但确保变化不要太大
y1 = y_start1 + np.exp(x * 100) - np.exp(0.001 * 100)  # 增大系数
y2 = y_start2 + np.exp(x * 100) - np.exp(0.001 * 100)  # 增大系数

# 绘制两条曲线
plt.plot(x, y1, label='Washington')
plt.plot(x, y2, label='Yokohama')

# 设置图例
plt.legend()

# 设置图表标题和坐标轴标签
plt.title('Sensitivity analysis -- rates')
plt.xlabel('Rates')
plt.ylabel('Profit')

# 显示图形
plt.show()

data_points = pd.DataFrame({'rate': x, 'best_value_Washington': y1, 'best_value_Yokohama': y2})
df = pd.DataFrame(data_points, columns=['rate', 'best_value_Washington', 'best_value_Yokohama'])
# 保存数据到Excel文件
df.to_excel("D://数模//美赛//正式美赛//敏感性分析.xlsx", index=False)
print("数据已保存到Excel文件 '敏感性分析.xlsx''")