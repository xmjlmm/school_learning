import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 定义目标函数
def objective_function(a, R, z):
    n = len(z)
    S_a = np.sum((z - a)**2) / (n - 1)
    D_a = np.sum([f(R - np.abs(z[i] - z[j])) for i in range(n) for j in range(i+1, n)])
    return S_a * D_a

# 定义f(t)函数
def f(t):
    if t > 0:
        return 1
    elif t == 0:
        return 0
    else:
        return 0

# 定义约束条件
def constraint_sum_to_one(a):
    return np.sum(a) - 1

def constraint_max_ra(a, R, z, m):
    r_a = np.max([np.abs(a[i] - a[j]) for i in range(len(a)) for j in range(i+1, len(a))])
    return 2*m - r_a - R

# 参数设置
n = 10  # 变量数量
R = 10  # 常量R
m = 5   # 常量m

# 定义随机初始数据
z = np.random.rand(n)

# 设置边界条件（所有变量a的取值范围是(0, 1)之间）
bounds = [(0, 1) for _ in range(n)]

# 定义约束条件
constraints = [
    {'type': 'eq', 'fun': constraint_sum_to_one},
    {'type': 'ineq', 'fun': lambda a: constraint_max_ra(a, R, z, m)}
]

# 保存每次迭代的目标函数值
history = []

# 目标函数的包装函数，记录每次调用时的函数值
def objective_function_with_logging(a):
    value = objective_function(a, R, z)
    history.append(value)
    return -value  # 因为我们使用的是最小化，所以返回负值

# 使用minimize方法求解
result = minimize(
    objective_function_with_logging,
    x0=np.random.rand(n),  # 初始解
    bounds=bounds,
    constraints=constraints,
    method='SLSQP',  # 使用Sequential Least Squares Programming (SLSQP)算法
    options={'disp': True}
)

# 打印结果
print("最优解 a:", result.x)
print("最优目标函数值 Q(a):", -result.fun)

# 绘制目标函数值随迭代次数的变化图
plt.figure(figsize=(10, 6))
plt.plot(history, marker='o', linestyle='-', color='b')
plt.title('Objective Function Value vs Iterations')
plt.xlabel('Iterations')
plt.ylabel('Objective Function Value')
plt.grid(True)
plt.show()
