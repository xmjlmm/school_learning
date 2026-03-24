import math
import random
import matplotlib.pyplot as plt

def func(x):
    return x**2 + math.sin(5*x)

def fitness(x):
    return 30-(x**2 + math.sin(5*x))

POPULATION_SIZE = 50
GENE_LENGTH = 16

def generate_population(population_size, gene_length):
    population = []
    for i in range(population_size):
        individual = [random.randint(0, 1) for j in range(gene_length)]
        population.append(individual)
    return population

population = generate_population(POPULATION_SIZE, GENE_LENGTH)

def crossover(parent1, parent2):
    crossover_point = random.randint(0, GENE_LENGTH - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutation(individual, mutation_probability):
    for i in range(GENE_LENGTH):
        if random.random() < mutation_probability:
            individual[i] = 1 - individual[i]
    return individual

def select_parents(population):
    total_fitness = sum([fitness(decode(individual)) for individual in population])
    parent1 = None
    parent2 = None
    while parent1 == parent2:
        parent1 = select_individual(population, total_fitness)
        parent2 = select_individual(population, total_fitness)
    return parent1, parent2

def select_individual(population, total_fitness):
    r = random.uniform(0, total_fitness)
    fitness_sum = 0
    for individual in population:
        fitness_sum += fitness(decode(individual))
        if fitness_sum > r:
            return individual
    return population[-1]

def decode(individual):
    x = sum([gene*2**i for i, gene in enumerate(individual)])
    return -5 + 10 * x / (2**GENE_LENGTH - 1)

def plot_evolution(fitness_values):
    plt.plot(fitness_values)
    plt.title('Evolution of Fitness Values')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.show()

GENERATIONS = 2000
CROSSOVER_PROBABILITY = 0.7
MUTATION_PROBABILITY = 0.1

# 在主循环中调用该函数，传入每一代的最佳适应度值
def genetic_algorithm():
    population = generate_population(POPULATION_SIZE, GENE_LENGTH)
    fitness_values = []  # 用于存储每一代的最佳适应度值
    for i in range(GENERATIONS):
        new_population = []
        for j in range(int(POPULATION_SIZE/2)):
            parent1, parent2 = select_parents(population)
            if random.random() < CROSSOVER_PROBABILITY:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            child1 = mutation(child1, MUTATION_PROBABILITY)
            child2 = mutation(child2, MUTATION_PROBABILITY)
            new_population.append(child1)
            new_population.append(child2)
        population = new_population
        best_individual = max(population, key=lambda individual: fitness(decode(individual)))
        best_fitness = fitness(decode(best_individual))
        fitness_values.append(best_fitness)

    # 绘制遗传算法的适应度值演变图
    plot_evolution(fitness_values)

    # 返回最终结果
    best_individual = max(population, key=lambda individual: fitness(decode(individual)))
    best_fitness = fitness(decode(best_individual))
    best_x = decode(best_individual)
    best_func = func(best_x)
    return best_x, best_fitness, best_func

# 在调用遗传算法的地方添加绘图代码
best_x, best_fitness, best_func = genetic_algorithm()

print("x = ", best_x)
print("最大适应度为", best_fitness)
print("函数值为", best_func)