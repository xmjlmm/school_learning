# import math
# from random import random
# import matplotlib.pyplot as plt
# import numpy as np
#
# def func(x, y):  # 函数优化问题
#     res = 4 * x ** 2 - 2.1 * x ** 4 + x ** 6 / 3 + x * y - 4 * y ** 2 + 4 * y ** 4
#     return res
#
#
# # x为公式里的x1,y为公式里面的x2
# class SA:
#     def __init__(self, func, iter=100, T0=100, Tf=0.01, alpha=0.99):
#         self.func = func
#         self.iter = iter  # 内循环迭代次数,即为L =100
#         self.alpha = alpha  # 降温系数，alpha=0.99
#         self.T0 = T0  # 初始温度T0为100
#         self.Tf = Tf  # 温度终值Tf为0.01
#         self.T = T0  # 当前温度
#         self.x = [random() * 11 - 5 for i in range(iter)]  # 随机生成100个x的值
#         self.y = [random() * 11 - 5 for i in range(iter)]  # 随机生成100个y的值
#         self.most_best = []
#         """
#         random()这个函数取0到1之间的小数
#         如果你要取0-10之间的整数（包括0和10）就写成 (int)random()*11就可以了，11乘以零点多的数最大是10点多，最小是0点多
#         该实例中x1和x2的绝对值不超过5（包含整数5和-5），（random() * 11 -5）的结果是-6到6之间的任意值（不包括-6和6）
#         （random() * 10 -5）的结果是-5到5之间的任意值（不包括-5和5），所有先乘以11，取-6到6之间的值，产生新解过程中，用一个if条件语句把-5到5之间（包括整数5和-5）的筛选出来。
#         """
#         self.history = {'f': [], 'T': []}
#
#     def generate_new(self, x, y):  # 扰动产生新解的过程
#         while True:
#             x_new = x + self.T * (random() - random())
#             y_new = y + self.T * (random() - random())
#             if (-5 <= x_new <= 5) & (-5 <= y_new <= 5):
#                 break  # 重复得到新解，直到产生的新解满足约束条件
#         return x_new, y_new
#
#     def Metrospolis(self, f, f_new):  # Metropolis准则
#         if f_new <= f:
#             return 1
#         else:
#             p = math.exp((f - f_new) / self.T)
#             if random() < p:
#                 return 1
#             else:
#                 return 0
#
#     def best(self):  # 获取最优目标函数值
#         f_list = []  # f_list数组保存每次迭代之后的值
#         for i in range(self.iter):
#             f = self.func(self.x[i], self.y[i])
#             f_list.append(f)
#         f_best = min(f_list)
#
#         idx = f_list.index(f_best)
#         return f_best, idx  # f_best,idx分别为在该温度下，迭代L次之后目标函数的最优解和最优解的下标
#
#     def run(self):
#         count = 0
#         # 外循环迭代，当前温度小于终止温度的阈值
#         while self.T > self.Tf:
#
#             # 内循环迭代100次
#             for i in range(self.iter):
#                 f = self.func(self.x[i], self.y[i])  # f为迭代一次后的值
#                 x_new, y_new = self.generate_new(self.x[i], self.y[i])  # 产生新解
#                 f_new = self.func(x_new, y_new)  # 产生新值
#                 if self.Metrospolis(f, f_new):  # 判断是否接受新值
#                     self.x[i] = x_new  # 如果接受新值，则把新值的x,y存入x数组和y数组
#                     self.y[i] = y_new
#             # 迭代L次记录在该温度下最优解
#             ft, _ = self.best()
#             self.history['f'].append(ft)
#             self.history['T'].append(self.T)
#             # 温度按照一定的比例下降（冷却）
#             self.T = self.T * self.alpha
#             count += 1
#
#             # 得到最优解
#         f_best, idx = self.best()
#         print(f"F={f_best}, x={self.x[idx]}, y={self.y[idx]}")
#
#
# sa = SA(func)
# sa.run()
#
# plt.plot(sa.history['T'], sa.history['f'])
# plt.title('SA')
# plt.xlabel('T')
# plt.ylabel('f')
# plt.gca().invert_xaxis()
# plt.show()
#
# #----------------------------------------------------------------------------------------------
#
# # 模拟退火求解
# Q = np.array(prediction_sales)  # 销量
# C = np.array(prediction_cost)  # 成本
# Loss = np.array([10.66463844, 12.73368135, 7.755571213, 6.411989175, 8.884176144, 8.911259058])
#
#
# # 模拟退火函数
# def simulated_annealing_maximize(initial_solution, temperature, cooling_rate, max_iterations, iter):
#     # 生成初始解
#     current_solution = initial_solution
#     best_solution = initial_solution
#     best_value = objective_function(best_solution, iter)
#
#     # 迭代
#     for iteration in range(max_iterations):
#         temperature *= cooling_rate
#
#         # 生成新的解
#         new_solution = generate_new_solution(current_solution, temperature, iter)
#
#         # 计算当前解和新解的目标函数值
#         current_value = objective_function(current_solution, iter)
#         new_value = objective_function(new_solution, iter)
#
#         # 计算目标函数值的差异
#         value_diff = new_value - current_value
#
#         # 判断是否接受新解，与爬山法的区别***********
#         if value_diff > 0 or random.random() < math.exp(value_diff / temperature):
#             current_solution = new_solution
#             current_value = new_value
#
#         # 更新最优解
#         if current_value > best_value:
#             best_solution = current_solution
#             best_value = current_value
#
#     return best_solution
#
#
# # 生成新的解的函数
# def generate_new_solution(solution, temperature, iter):
#     y = [random.randint(1, 100) for _ in range(6)]
#     y = np.array(y)
#     z = y / math.sqrt(np.sum(np.sqrt(y)))
#     new_solution = solution + (z * temperature)
#     for i in range(6):
#         if new_solution[i] < C[i, iter] * 1.2 or new_solution[i] > C[i, iter] * 1.5:
#             random_float = random.random()
#             new_solution[i] = C[i, iter] * 1.1 + 0.4 * C[i, iter] * random_float
#     return new_solution
#
#
# # 目标函数
# def objective_function(solution, iter):
#     P = np.array(solution)
#     y = (P - C[:, iter]) * Q[:, iter] * (1.0 - Loss) + (0.8 * solution - C[:, iter]) * Q[:, iter] * Loss
#     return sum(y)
#
#
# begin_solution = np.array([9, 9, 9, 9, 9, 9])
#
# rows = 7
# cols = 6
# result = [[0] * cols for _ in range(rows)]
# for iter in range(7):
#     ans = simulated_annealing_maximize(begin_solution, 1000, 0.95, 200, iter)
#     result[iter] = ans
#
# plt.figure()
# price = np.array(result)
# for i in range(6):
#     x = range(1,8)
#     plt.plot(x,price[:,i])


# import math
# from random import random
# import matplotlib.pyplot as plt
# import numpy as np
#
# # 以下为您提供的代码，请勿更改
#
# # 模拟退火函数
# def simulated_annealing_maximize(initial_solution, temperature, cooling_rate, max_iterations, iter):
#     # 生成初始解
#     current_solution = initial_solution
#     best_solution = initial_solution
#     best_value = objective_function(best_solution, iter)
#
#     # 迭代
#     for iteration in range(max_iterations):
#         temperature *= cooling_rate
#
#         # 生成新的解
#         new_solution = generate_new_solution(current_solution, temperature, iter)
#
#         # 计算当前解和新解的目标函数值
#         current_value = objective_function(current_solution, iter)
#         new_value = objective_function(new_solution, iter)
#
#         # 计算目标函数值的差异
#         value_diff = new_value - current_value
#
#         # 判断是否接受新解，与爬山法的区别***********
#         if value_diff > 0 or random.random() < math.exp(value_diff / temperature):
#             current_solution = new_solution
#             current_value = new_value
#
#         # 更新最优解
#         if current_value > best_value:
#             best_solution = current_solution
#             best_value = current_value
#
#     return best_solution
#
# # 生成新的解的函数
# def generate_new_solution(solution, temperature, iter):
#     y = [random.randint(1, 100) for _ in range(6)]
#     y = np.array(y)
#     z = y / math.sqrt(np.sum(np.sqrt(y)))
#     new_solution = solution + (z * temperature)
#     for i in range(6):
#         if new_solution[i] < C[i, iter] * 1.2 or new_solution[i] > C[i, iter] * 1.5:
#             random_float = random.random()
#             new_solution[i] = C[i, iter] * 1.1 + 0.4 * C[i, iter] * random_float
#     return new_solution
#
# # 目标函数
# def objective_function(solution, iter):
#     P = np.array(solution)
#     y = (P - C[:, iter]) * Q[:, iter] * (1.0 - Loss) + (0.8 * solution - C[:, iter]) * Q[:, iter] * Loss
#     return sum(y)
#
# # 以下为新增的部分，请根据您的需求进行调整
#
# # 初始化销量、成本和损失数据
# prediction_sales = [100, 200, 150, 300, 250, 180]  # 示例销量数据
# prediction_cost = [50, 60, 45, 70, 55, 65]  # 示例成本数据
#
# Q = np.array(prediction_sales)  # 销量
# C = np.array(prediction_cost)  # 成本
# Loss = np.array([10.66463844, 12.73368135, 7.755571213, 6.411989175, 8.884176144, 8.911259058])
#
# # 初始化求解结果存储列表
# result = []
#
# # 迭代7次，每次调用模拟退火算法求解并记录结果
# for iter in range(7):
#     # 设置初始解
#     begin_solution = np.array([9, 9, 9, 9, 9, 9])
#     # 使用模拟退火算法求解
#     ans = simulated_annealing_maximize(begin_solution, 1000, 0.95, 200, iter)
#     # 将结果添加到结果列表中
#     result.append(ans)
#
# # 绘制结果图表
# plt.figure()
# price = np.array(result)
# for i in range(6):
#     x = range(1, 8)
#     plt.plot(x, price[:, i])
#
# # 显示图表
# plt.xlabel('Iteration')
# plt.ylabel('Price')
# plt.title('Simulated Annealing Result')
# plt.show()


# import math
# from random import random, randint
# import matplotlib.pyplot as plt
# import numpy as np
# from matplotlib.font_manager import FontProperties
#
# # 目标函数
# def objective_function(x, y):
#     return -x**2 - y**2  # 最大化该函数的值，因此加负号
#
# # 定义初始解生成函数
# def generate_initial_solution():
#     return randint(-10, 10), randint(-10, 10)  # 随机生成初始解的x、y值
#
# # 定义新解生成函数
# def generate_new_solution(x, y, temperature):
#     new_x = x + (random() - 0.5) * temperature
#     new_y = y + (random() - 0.5) * temperature
#     return new_x, new_y
#
# # Metropolis准则
# def metropolis(current_value, new_value, temperature):
#     if new_value > current_value:
#         return True
#     else:
#         probability = math.exp((new_value - current_value) / temperature)
#         return random() < probability
#
# # 模拟退火算法迭代部分
# def simulated_annealing(obj_func, max_iterations = 50, initial_temperature = 100, cooling_rate = 0.95):
#     current_x, current_y = generate_initial_solution()
#     current_value = obj_func(current_x, current_y)
#     best_solution = (current_x, current_y)
#     best_value = current_value
#     temperature = initial_temperature
#     value_history = []
#
#
#     for iteration in range(0, max_iterations):
#         temperature *= cooling_rate
#         new_x, new_y = generate_new_solution(current_x, current_y, temperature)
#         new_value = obj_func(new_x, new_y)
#         if metropolis(current_value, new_value, temperature):
#             current_x, current_y = new_x, new_y
#             current_value = new_value
#             if new_value > best_value:
#                 best_solution = (current_x, current_y)
#                 best_value = new_value
#         value_history.append(best_value)
#
#     return best_solution, value_history
#
#
# def main():
#     # 求解目标函数的最大值
#     best_solution, value_history = simulated_annealing(objective_function)
#     font = FontProperties(fname=r"c:\windows\fonts\SimSun.ttc", size=15)
#
#     # 输出最优解及其对应的函数值
#     print("最优解：", best_solution)
#     print("最优值：", objective_function(*best_solution))
#
#     # 绘制函数值随迭代次数变化的曲线图
#     plt.plot(value_history)
#     plt.xlabel("迭代次数", font = font)
#     plt.ylabel("函数值", font = font)
#     plt.title("模拟退火算法优化过程", font = font)
#     plt.show()
#
# # 调试代码部分
# if __name__ == "__main__":
#     main()


import math
from random import random, randint
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties


# 目标函数
def objective_function(x, y):
    return -x ** 2 - y ** 2  # 最大化该函数的值，因此加负号


# 约束条件函数
def constraint(x, y):
    # 示例约束条件：x + y <= 10
    return x + y <= 10 and x ** 2 + y ** 2 >= 20


# 定义初始解生成函数
def generate_initial_solution():
    return randint(-10, 10), randint(-10, 10)  # 随机生成初始解的x、y值


# 定义新解生成函数
def generate_new_solution(x, y, temperature):
    new_x = x + (random() - 0.5) * temperature
    new_y = y + (random() - 0.5) * temperature
    return new_x, new_y


# Metropolis准则
def metropolis(current_value, new_value, temperature):
    if new_value > current_value:
        return True
    else:
        probability = math.exp((new_value - current_value) / temperature)
        return random() < probability


# 模拟退火算法迭代部分
def simulated_annealing(obj_func, constraint_func, max_iterations=50, initial_temperature=100, cooling_rate=0.95):
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
            if new_value > best_value:
                best_solution = (current_x, current_y)
                best_value = new_value
        value_history.append(best_value)

    return best_solution, value_history


def main():
    # 求解目标函数的最大值
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
