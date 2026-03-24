import numpy as np
import pandas as pd

def entropy_weight(data):
    """
    熵权法计算权重
    参数:
    data - 二维数组，表示各指标下的评价对象
    返回:
    权重数组
    """
    # 数据标准化处理
    data = data / data.sum(axis=0)

    # 计算每个指标的熵值
    k = 1.0 / np.log(data.shape[0])
    entropy = -k * ((data * np.log(data)).sum(axis=0))

    # 计算权重
    weight = (1 - entropy) / (1 - entropy).sum()

    return weight

def coefficient_of_variation(data):
    """
    变异系数法计算权重
    参数:
    data - 二维数组，表示各指标下的评价对象
    返回:
    权重数组
    """
    # 计算各指标的标准差和平均值
    std_dev = np.std(data, axis=0)
    mean = np.mean(data, axis=0)

    # 计算变异系数
    cv = std_dev / mean

    # 归一化处理
    weight = cv / cv.sum()

    return weight

# 示例数据
data = np.array([
    [3, 5, 2],
    [4, 4, 6],
    [5, 3, 7]
])

# 计算熵权法和变异系数法的权重
entropy_weights = entropy_weight(data)
cv_weights = coefficient_of_variation(data)

# 结合两种方法的权重
combined_weights = (entropy_weights + cv_weights) / 2

# 输出结果
print("熵权法权重:", entropy_weights)
print("变异系数法权重:", cv_weights)
print("结合后的权重:", combined_weights)
