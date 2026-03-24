import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 目标函数（目标是最小化该函数，因此取负值以实现最小化）
def objective_function(x, y):
    return x ** 2 + 1 / (y ** 2) + 1 / (x ** 2 + y ** 2)

# 约束条件函数
def constraint(x, y):
    return x + y < 3 and x > 0 and y > 0 and x < 4 and y < 4

# 初始化种群
def initialize_population(pop_size, x_bounds, y_bounds):
    return [(random.uniform(*x_bounds), random.uniform(*y_bounds)) for _ in range(pop_size)]

# 计算适应度（对于最小化问题，适应度为目标函数的负值）
def evaluate_population(population):
    return [-objective_function(x, y) for x, y in population]  # 取负值以便最大化负目标函数值

# def evaluate_population(population):
#     return [objective_function(x, y) for x, y in population]

# 选择操作（轮盘赌选择）
def select_population(population, fitness_scores, num_individuals):
    sorted_indices = np.argsort(fitness_scores)[::-1]
    selected_indices = sorted_indices[:num_individuals]
    return [population[i] for i in selected_indices]

# 交叉操作
def crossover(parent1, parent2):
    x1, y1 = parent1
    x2, y2 = parent2
    return (x1, y2), (x2, y1)

# 变异操作
def mutate(individual, mutation_rate, x_bounds, y_bounds):
    x, y = individual
    if random.random() < mutation_rate:
        x = random.uniform(*x_bounds)
    if random.random() < mutation_rate:
        y = random.uniform(*y_bounds)
    return x, y

# 遗传算法
def genetic_algorithm(obj_func, constraint_func, pop_size=50, num_generations=100, mutation_rate=0.1, x_bounds=(0, 4), y_bounds=(0, 4)):
    population = initialize_population(pop_size, x_bounds, y_bounds)

    best_solution = None
    best_value = float('inf')  # 对于最小化问题，初始值应为正无穷
    value_history = []

    for generation in range(num_generations):
        fitness_scores = evaluate_population(population)
        valid_indices = [i for i in range(pop_size) if constraint_func(*population[i])]

        # 保留符合约束条件的个体
        valid_population = [population[i] for i in valid_indices]
        valid_fitness_scores = [fitness_scores[i] for i in valid_indices]

        if valid_population:
            best_idx = np.argmin(valid_fitness_scores)  # 最小化目标函数，找到最小值索引
            best_candidate = valid_population[best_idx]
            best_candidate_value = -valid_fitness_scores[best_idx]  # 恢复原目标函数值

            if best_candidate_value < best_value:
                best_solution = best_candidate
                best_value = best_candidate_value

        value_history.append(best_value)

        selected = select_population(valid_population, valid_fitness_scores, min(pop_size // 2, len(valid_population)))

        new_population = []
        while len(new_population) < pop_size:
            if len(selected) < 2:
                break
            parent1, parent2 = random.sample(selected, 2)
            offspring1, offspring2 = crossover(parent1, parent2)
            new_population.append(mutate(offspring1, mutation_rate, x_bounds, y_bounds))
            new_population.append(mutate(offspring2, mutation_rate, x_bounds, y_bounds))

        population = new_population

    return best_solution, value_history

def main():
    # 求解目标函数的最小值
    best_solution, value_history = genetic_algorithm(objective_function, constraint)
    font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=15)

    # 输出最优解及其对应的函数值
    print("最优解：", best_solution)
    print("最优值：", objective_function(*best_solution))

    # 绘制函数值随代数变化的曲线图
    plt.plot(value_history)
    plt.xlabel("代数", fontproperties=font)
    plt.ylabel("函数值", fontproperties=font)
    plt.title("遗传算法优化过程", fontproperties=font)
    plt.show()

if __name__ == "__main__":
    main()
