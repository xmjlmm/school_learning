import numpy as np
import matplotlib.pyplot as plt

# 函数定义
def f(x):
    return np.sum(x**2)

# 适应度函数（转换为最大化问题）
def fitness_function(individual):
    return -f(individual)  # 适应度是负的函数值

# 选择函数（轮盘赌选择）
def selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    probabilities = [fit / total_fitness for fit in fitness_values]
    return population[np.random.choice(len(population), p=probabilities)]

# 交叉函数
def crossover(parent1, parent2, cross_rate):
    if np.random.rand() < cross_rate:
        alpha = np.random.rand()
        child1 = alpha * parent1 + (1 - alpha) * parent2
        child2 = (1 - alpha) * parent1 + alpha * parent2
    else:
        child1, child2 = parent1.copy(), parent2.copy()
    return child1, child2

# 变异函数
def mutate(individual, mutation_rate, lower_bound, upper_bound):
    for i in range(len(individual)):
        if np.random.rand() < mutation_rate:
            individual[i] += np.random.uniform(-1, 1)  # 小幅度随机变动
            individual[i] = np.clip(individual[i], lower_bound, upper_bound)  # 保证在范围内
    return individual

# 遗传算法主函数
def genetic_algorithm(population_size, generations, mutation_rate, cross_rate, lower_bound=-20, upper_bound=20, dimensions=10):
    # 初始化种群
    population = np.random.uniform(lower_bound, upper_bound, (population_size, dimensions))

    best_fitness_over_time = []
    best_fitness = float('-inf')
    best_solution = None

    for generation in range(generations):
        fitness_values = [fitness_function(individual) for individual in population]

        # 更新最佳适应度和解
        for i, fitness in enumerate(fitness_values):
            if fitness > best_fitness:  # 注意这里是适应度最大化
                best_fitness = fitness
                best_solution = population[i]

        best_fitness_over_time.append(best_fitness)

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
        population = [mutate(individual, mutation_rate, lower_bound, upper_bound) for individual in new_population]

    return best_solution, best_fitness, best_fitness_over_time

def main():
    best_x, best_fitness, best_fitness_over_time = genetic_algorithm(
        population_size=2000,
        generations=100,
        mutation_rate=0.6,
        cross_rate=0.7
    )
    print(f"最佳解 x: {best_x}, 最优值 f(x): {-best_fitness}")  # 打印最小化的目标函数值

    # 可视化
    plt.plot(best_fitness_over_time, label='Best Fitness Over Generations')
    plt.title('Fitness Evolution Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness')
    plt.legend()
    plt.grid()
    plt.show()

main()
