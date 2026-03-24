import random
import math

# 定义免疫算法类
class ImmuneAlgorithm:
    def __init__(self, min_x, max_x, population_size, max_iterations, mutation_rate):
        self.min_x = min_x                # x 的最小值
        self.max_x = max_x                # x 的最大值
        self.population_size = population_size  # 种群大小
        self.max_iterations = max_iterations    # 最大迭代次数
        self.mutation_rate = mutation_rate      # 突变概率

    # 适应度函数（在这里是 f(x) = x^2）
    def fitness(self, x):
        return x ** 2

    # 初始化种群
    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            x = random.uniform(self.min_x, self.max_x)
            population.append(x)
        return population

    # 选择操作（在这里是锦标赛选择）
    def selection(self, population):
        tournament_size = 3  # 锦标赛规模
        selected = []
        for _ in range(self.population_size):
            tournament = random.sample(population, tournament_size)
            winner = max(tournament, key=lambda x: self.fitness(x))
            selected.append(winner)
        return selected

    # 突变操作
    def mutation(self, individual):
        if random.random() < self.mutation_rate:
            mutation_amount = random.uniform(-0.1, 0.1)  # 随机生成突变量
            individual += mutation_amount
            individual = max(min(individual, self.max_x), self.min_x)  # 确保个体在指定范围内
        return individual

    # 运行免疫算法
    def run(self):
        population = self.initialize_population()

        for iteration in range(self.max_iterations):
            # 选择操作
            selected = self.selection(population)

            # 突变操作
            mutated = [self.mutation(individual) for individual in selected]

            # 更新种群
            population = mutated

            # 输出每次迭代的最优解
            best_individual = max(population, key=lambda x: self.fitness(x))
            print(f"Iteration {iteration + 1}: Best Solution = {best_individual}, Fitness = {self.fitness(best_individual)}")

        # 输出最终结果
        best_individual = max(population, key=lambda x: self.fitness(x))
        print(f"Final Solution: {best_individual}, Fitness = {self.fitness(best_individual)}")

def main():
    min_x = -10    # x 的最小值
    max_x = 10     # x 的最大值
    population_size = 50  # 种群大小
    max_iterations = 100   # 最大迭代次数
    mutation_rate = 0.1    # 突变概率

    # 创建免疫算法对象并运行
    ia = ImmuneAlgorithm(min_x, max_x, population_size, max_iterations, mutation_rate)
    ia.run()

# 示例
if __name__ == "__main__":
    main()