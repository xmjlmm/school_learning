import numpy as np
from scipy.optimize import NonlinearConstraint, minimize
from platypus import NSGAII, Problem, Real, nondominated


# 定义目标函数
def objective_function(x):
    VA, VB, VC, P = x[0], x[1], x[2], x[3]
    f1 = VA - VB  # 最大化VA - VB
    f2 = VC  # 最小化VC
    return [f1, f2]


# 定义约束函数
def constraints(x):
    VA, VB, VC, P = x[0], x[1], x[2], x[3]

    # 添加你的约束函数
    c1 = VA + VB + VC - P - 1.5  # 示例约束
    c2 = VA * VB - VC - 2.0  # 示例约束
    return [c1, c2]


# 定义优化问题
problem = Problem(4, 2, 2)  # 4个变量，2个目标函数，2个约束
problem.types[:] = Real(0, 10)  # 变量取值范围
problem.constraints[:] = ">=0"
problem.function = objective_function
problem.constraints_func = constraints

# 使用NSGAII求解
algorithm = NSGAII(problem)
algorithm.run(10000)

# 获取帕累托前沿
solutions = nondominated(algorithm.result)

# 打印结果
for solution in solutions:
    print("决策变量:", solution.variables)
    print("目标值:", solution.objectives)
