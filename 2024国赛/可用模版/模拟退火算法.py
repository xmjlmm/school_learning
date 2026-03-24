# x^2 + 1/(y^2) + 1/(x^2+y^2)

import math
# from random import random, randint
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# 目标函数
def objective_function(x, y):
    return x ** 2 + 1 / (y ** 2) + 1/ (x ** 2+y ** 2)  # 最大化该函数的值，因此加负号


# 约束条件函数
def constraint(x, y):
    # 示例约束条件：x + y <= 10
    return x + y < 3 and x > 0 and x < 4 and y > 0 and y < 4


# 定义初始解生成函数
def generate_initial_solution():
    x, y = 4 * random.random(), 4 * random.random()
    while x == 0:
        x = 4 * random.random()
    while y == 0:
        y = 4 * random.random()
    return x, y # 随机生成初始解的x、y值


# 定义新解生成函数
def generate_new_solution(x, y, temperature):
    new_x = x + (random.random() - 0.5) * temperature
    new_y = y + (random.random() - 0.5) * temperature
    return new_x, new_y


# Metropolis准则
def metropolis(current_value, new_value, temperature):
    if new_value < current_value:
        return True
    else:
        probability = math.exp((new_value - current_value) / temperature)
        return random.random() < probability


# 模拟退火算法迭代部分
def simulated_annealing(obj_func, constraint_func, max_iterations=200, initial_temperature=1000, cooling_rate=0.95):
    current_x, current_y = generate_initial_solution()
    current_value = obj_func(current_x, current_y)
    best_solution = (current_x, current_y)
    best_value = current_value
    temperature = initial_temperature
    value_history = []

    for iteration in range(max_iterations):
        temperature *= cooling_rate
        new_x, new_y = generate_new_solution(current_x, current_y, temperature)

        # 约束条件检查
        if not constraint_func(new_x, new_y):
            continue  # 如果不满足约束条件，则跳过此解

        new_value = obj_func(new_x, new_y)
        if metropolis(current_value, new_value, temperature):
            current_x, current_y = new_x, new_y
            current_value = new_value
            if new_value < best_value:
                best_solution = (current_x, current_y)
                best_value = new_value
        value_history.append(best_value)

    return best_solution, value_history


def main():
    # 求解目标函数的最小值
    best_solution, value_history = simulated_annealing(objective_function, constraint)
    font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=15)

    # 输出最优解及其对应的函数值
    print("最优解：", best_solution)
    print("最优值：", objective_function(*best_solution))

    # 绘制函数值随迭代次数变化的曲线图
    plt.plot(value_history)
    plt.xlabel("迭代次数", fontproperties=font)
    plt.ylabel("函数值", fontproperties=font)
    plt.title("模拟退火算法优化过程", fontproperties=font)
    plt.show()


# 调试代码部分
if __name__ == "__main__":
    main()



