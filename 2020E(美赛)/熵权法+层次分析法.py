import numpy as np

def entropy_weight(data):
    """
    计算熵权法的权重

    参数:
    data - 二维数组，表示各个指标下的评价对象

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

def AHP(criteria, b):
    """
    层次分析法（AHP）

    参数:
    criteria - 判断矩阵
    b - 一致性指标随机一致性指数的值

    返回:
    权重向量和一致性比率CR
    """
    # 计算判断矩阵的特征值和特征向量
    eig_val, eig_vec = np.linalg.eig(criteria)
    max_eig_val = np.max(eig_val)
    max_eig_vec = eig_vec[:, eig_val.argmax()]

    # 权重向量
    weights = max_eig_vec / max_eig_vec.sum()

    # 一致性检验
    CI = (max_eig_val - len(criteria)) / (len(criteria) - 1)
    CR = CI / b

    return weights, CR

# 示例数据
# 指标层判断矩阵
criteria = np.array([[1, 1/3, 3],
                     [3, 1, 5],
                     [1/3, 1/5, 1]])

# 指标随机一致性指数RI（这里假设为3x3矩阵的RI值）
RI = 0.58

# 评价对象在各指标下的得分
data = np.array([[0.8, 0.6, 0.7],
                 [0.9, 0.8, 0.6],
                 [0.6, 0.7, 0.8]])

# 计算层次分析法的权重和一致性比率
ahp_weights, CR = AHP(criteria, RI)

# 输出结果
print("AHP权重：", ahp_weights.real)
print("一致性比率：", CR.real)
