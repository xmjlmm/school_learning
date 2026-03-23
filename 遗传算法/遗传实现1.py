# 编程实现遗传算法（要求采用二进制编码）在解空间内进行最优解搜索
# 0≤x≤10
# f(x)=x+10sin(5x)+7cos(4x)

import numpy as np
import matplotlib.pyplot as plt

# 函数定义
def f(x):
    return x + 10 * np.sin(5 * x) + 7 * np.cos(4 * x)

# 将二进制字符串转换为实数
def binary_to_decimal(binary_str, lower_bound, upper_bound):
    decimal_value = int(binary_str, 2)
    return lower_bound + (upper_bound - lower_bound) * decimal_value / (2 ** len(binary_str) - 1)

# 适应度函数
def fitness_function(binary_str, lower_bound=0, upper_bound=10):
    x = binary_to_decimal(binary_str, lower_bound, upper_bound)
    return f(x)

# 选择函数（轮盘赌选择）
def selection(population, fitness_values):
    min_fitness = min(fitness_values)
    max_fitness = max(fitness_values)
    fitness_values = [(f - min_fitness) / (max_fitness - min_fitness) for f in fitness_values]  # 调整，使得所有值非负

    total_fitness = sum(fitness_values)
    probabilities = [i / total_fitness for i in fitness_values]  # 计算选择概率
    return population[np.random.choice(len(population), p=probabilities)]

# 交叉函数
def crossover(parent1, parent2, cross_rate):
    if np.random.rand() < cross_rate:
        point = np.random.randint(1, len(parent1) - 1)  # 选择交叉点
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
    else:
        child1, child2 = parent1, parent2  # 没有交叉时直接复制
    return child1, child2

# 变异函数
def mutate(binary_str, mutation_rate):
    new_str = ''
    for gene in binary_str:
        if np.random.rand() < mutation_rate:
            new_str += '0' if gene == '1' else '1'
        else:
            new_str += gene
    return new_str

# 遗传算法主函数
def genetic_algorithm(population_size, generations, mutation_rate, cross_rate, lower_bound=0, upper_bound=10):
    # 初始化种群
    population = [''.join(np.random.choice(['0', '1']) for _ in range(10)) for _ in range(population_size)]

    best_fitness_over_time = []  # 存储每一代的最佳适应度
    best_fitness = -np.inf
    best_solution = None

    for generation in range(generations):
        fitness_values = [fitness_function(individual) for individual in population]

        # 更新最佳适应度和解
        for i, fitness in enumerate(fitness_values):
            if fitness > best_fitness:
                best_fitness = fitness
                best_solution = population[i]

        best_fitness_over_time.append(best_fitness)  # 记录最佳适应度

        # 选择
        selected_population = [selection(population, fitness_values) for _ in range(population_size)]

        # 交叉
        new_population = []
        for i in range(0, population_size, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i + 1]
            child1, child2 = crossover(parent1, parent2, cross_rate)
            new_population.extend([child1, child2])

        # 变异
        population = [mutate(individual, mutation_rate) for individual in new_population]

    # 返回最佳解和每代最佳适应度
    best_x = binary_to_decimal(best_solution, lower_bound, upper_bound)
    return best_x, best_fitness, best_fitness_over_time

def main():
    # 运行遗传算法
    best_x, best_fitness, best_fitness_over_time = genetic_algorithm(population_size=100, generations=100,
                                                                     mutation_rate=0.01, cross_rate=0.5)
    print(f"最佳解 x: {best_x:.4f}, 最优值 f(x): {best_fitness:.4f}")

    # 可视化函数
    x_values = np.linspace(0, 10, 400)
    y_values = f(x_values)
    plt.plot(x_values, y_values, label='f(x) = x + 10sin(5x) + 7cos(4x)')
    plt.scatter(best_x, best_fitness, color='red', label='Best Solution')
    plt.title('Genetic Algorithm Optimization')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid()
    plt.show()

    # 绘制迭代曲线
    plt.plot(best_fitness_over_time, label='Best Fitness Over Generations')
    plt.title('Fitness Evolution Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.legend()
    plt.grid()
    plt.show()


main()
