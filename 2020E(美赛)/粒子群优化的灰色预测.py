import numpy as np
from scipy.optimize import differential_evolution

def GM11(x0):
    """
    灰色预测模型GM(1,1)
    参数:
    x0 - 原始数据序列
    返回:
    预测结果
    """
    x1 = np.cumsum(x0)  # 一次累加序列
    z1 = (x1[:-1] + x1[1:]) / 2  # 紧邻均值生成序列
    B = np.array([-z1, np.ones(len(z1))]).T
    Y = x0[1:]

    # 最小二乘估计参数
    A = np.linalg.inv(B.T.dot(B)).dot(B.T).dot(Y)
    a, b = A[0], A[1]

    # 构建模型并预测
    f = lambda k: (x0[0] - b / a) * np.exp(-a * (k - 1)) - (x0[0] - b / a) * np.exp(-a * (k - 2))
    return np.array([f(i) for i in range(1, len(x0) + 1)])

def fitness_function(A):
    """
    适应度函数
    参数:
    A - 优化算法的参数
    返回:
    误差值
    """
    # 用优化算法的参数调整原始数据
    x0 = np.array([i * A[0] for i in raw_data])
    x_pred = GM11(x0)
    return np.mean(np.abs((x_pred - raw_data) / raw_data))  # 计算平均绝对百分比误差

# 原始数据
raw_data = np.array([225, 226, 228, 235, 241])

# 微分进化优化
bounds = [(0.1, 10.0)]  # 参数范围
result = differential_evolution(fitness_function, bounds)

# 使用优化后的参数进行预测
optimized_data = np.array([i * result.x[0] for i in raw_data])
prediction = GM11(optimized_data)

# 输出结果
print("优化后的参数:", result.x)
print("预测结果:", prediction)
