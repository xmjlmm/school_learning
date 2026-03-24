import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import matplotlib.pyplot as plt
import time  ##1##

# 1. 数据准备
data = pd.read_excel("D://数模//美赛//排位赛//问题一.xlsx")
data = data.dropna()
# 后三列作为 y
y = data.iloc[:, -3:]
# 前九列作为 x
X = data.iloc[:, :9]
# np.random.seed(42)
# X = np.random.rand(5000, 5)
# y = np.random.rand(5000, 1)


now_time = time.time()  ##2##

# 2. 构建BP神经网络模型
def create_model():
    model = Sequential([
        Dense(9, input_dim=9, activation='relu'),
        Dense(12, activation='sigmoid'),
        Dense(3, activation='relu')
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# 3. 实现遗传算法
def genetic_algorithm(model, X, y, population_size=50, generations=10):
    # 初始化种群
    population = [model.get_weights() for _ in range(population_size)]

    for generation in range(generations):
        # 评估种群
        fitness = []
        for weights in population:
            model.set_weights(weights)
            loss = model.evaluate(X, y, verbose=0)
            fitness.append(1 / (loss + 1e-8))

        # 选择（轮盘赌选择）
        fitness_sum = sum(fitness)

        prob = [f / fitness_sum for f in fitness]
        selected_indices = np.random.choice(range(population_size), size=population_size, replace=True, p=prob)
        selected_population = [population[i] for i in selected_indices]

        # 交叉和变异
        new_population = []
        for i in range(0, population_size, 2):
            parent1, parent2 = selected_population[i], selected_population[i+1]
            child1, child2 = crossover(parent1, parent2)  # 自定义交叉函数
            child1 = mutate(child1)  # 自定义变异函数
            child2 = mutate(child2)
            new_population.extend([child1, child2])

        population = new_population

    # 返回最佳个体
    best_index = np.argmax(fitness)
    return population[best_index]

def crossover(parent1, parent2):
    # 简单的权重平均交叉
    child1 = [(p1 + p2) / 2 for p1, p2 in zip(parent1, parent2)]
    child2 = [(p1 + p2) / 2 for p1, p2 in zip(parent1, parent2)]
    return child1, child2

def mutate(weights, mutation_rate=0.06):
    # 随机变异
    new_weights = []
    for w in weights:
        if np.random.rand() < mutation_rate:
            new_weights.append(w * np.random.normal(loc=5, scale=0.0, size=w.shape))
            # loc : 也叫做 mu，表示生成的正态分布的均值，对应这里的数学概念期望。
            # scale : 也叫做 sigma，表示这个分布的标准差。
        else:
            new_weights.append(w)
    return new_weights

# 4. 模型训练与评估
model = create_model()
best_weights = genetic_algorithm(model, X, y)
model.set_weights(best_weights)
history = model.fit(X, y, epochs=100, verbose=1) # verbose为输出日志
mse = history.history['loss']

total_time = time.time() - now_time  ##3##
print("total_time", total_time)  ##4##

# 5. 结果可视化
plt.plot(mse)
plt.title('MSE')
plt.xlabel('iterations')
plt.ylabel('MSE')
plt.show()


