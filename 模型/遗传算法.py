import numpy as np
import matplotlib.pyplot as plt

# 遗传算法参数
DNA_SIZE = 8  # 染色体长度
POP_SIZE = 200  # 种群大小
CROSSVER_RATE = 0.9  # 交叉概率
MUTATION_RATE = 0.01  # 变异概率
N_GENERATIONS = 5000  # 迭代次数
X_BOUND = [0.00, 4]  # x的取值范围
Y_BOUND = [0.00, 4]  # y的取值范围


# 定义目标函数
def objective_function(x, y):
    epsilon = 1e1
    x = np.where(x == 0, epsilon, x)
    y = np.where(y == 0, epsilon, y)
    return x ** 2 + 1 / (y ** 2) + 1 / (x ** 2 + y ** 2)


# 计算适应度
def calculate_fitness(pop):
    x, y = decode_population(pop)
    pred = objective_function(x, y)

    # 计算适应度
    fitness = pred - np.min(pred) + 1e-3
    return fitness


# 定义约束条件
def constraint_penalty(x, y):
    penalty = (x + y >= 3) # 增强惩罚系数
    return penalty


# 解码函数
def decode_population(pop):
    x_pop = pop[:, 1::2]  # pop中的奇数列表示x
    y_pop = pop[:, 0::2]  # pop中的偶数列表示y
    x = x_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (X_BOUND[1] - X_BOUND[0]) + X_BOUND[0]
    y = y_pop.dot(2 ** np.arange(DNA_SIZE)[::-1]) / float(2 ** DNA_SIZE - 1) * (Y_BOUND[1] - Y_BOUND[0]) + Y_BOUND[0]
    return x, y


# 交叉和变异操作
def crossover_and_mutation(pop, CROSSVER_RATE=0.8):
    new_pop = []
    for father in pop:
        child = father.copy()
        if np.random.rand() < CROSSVER_RATE:
            mother = pop[np.random.randint(POP_SIZE)]
            cross_points = np.random.randint(low=0, high=DNA_SIZE * 2)
            child[cross_points:] = mother[cross_points:]
        mutation(child)
        new_pop.append(child)
    return new_pop


# 变异操作
def mutation(child, MUTATION_RATE=0.1):
    if np.random.rand() < MUTATION_RATE:
        mutate_points = np.random.randint(0, DNA_SIZE * 2)
        child[mutate_points] = child[mutate_points] ^ 1


# 选择操作
def select(pop, fitness):
    fitness_sum = fitness.sum()
    if fitness_sum == 0:
        fitness = np.ones_like(fitness)
    else:
        fitness = fitness / fitness_sum  # 正常化适应度

    idx = np.random.choice(np.arange(POP_SIZE), size=POP_SIZE, replace=True, p=fitness)
    return pop[idx]


# 打印信息
def print_info(pop):
    x, y = decode_population(pop)
    fitness = calculate_fitness(pop)
    penalty = constraint_penalty(x, y)
    fitness_with_penalty = fitness - penalty
    fitness_with_penalty = np.maximum(fitness_with_penalty, 0)  # 确保适应度不为负数
    max_fitness_index = np.argmax(fitness_with_penalty)
    print('max_fitness:%s,函数最大值:%s' % (
        fitness_with_penalty[max_fitness_index], objective_function(x[max_fitness_index], y[max_fitness_index])))


# 初始化记录适应度数据
best_fitness_per_generation = []

if __name__ == '__main__':
    pop = np.random.randint(2, size=(POP_SIZE, DNA_SIZE * 2))
    for i in range(N_GENERATIONS):
        pop = np.array(crossover_and_mutation(pop))  # 交叉变异
        fitness = calculate_fitness(pop)  # 得到适应度
        penalty = constraint_penalty(*decode_population(pop))
        fitness -= penalty  # 加入约束条件的惩罚
        fitness = np.maximum(fitness, 0)  # 确保适应度不为负数
        pop = select(pop, fitness)  # 优胜劣汰

        # 记录每代的最佳适应度
        best_fitness_per_generation.append(np.max(fitness))

        if i % 100 == 0:
            print('第%s次迭代:' % i)
            print_info(pop)

    # 绘制迭代图
    plt.figure(figsize=(10, 6))
    plt.plot(best_fitness_per_generation, label='Best Fitness per Generation')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.title('Fitness Evolution Over Generations')
    plt.legend()
    plt.grid(True)
    plt.show()

    print_info(pop)
