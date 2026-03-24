'''麻雀搜索算法'''
import numpy as np
import copy


def initial(pop, dim, ub, lb):
    X = np.random.uniform(low=lb, high=ub, size=(pop, dim))
    return X


def CaculateFitness(X, param):
    pass


def SSA(pop, dim, lb, ub, Max_iter):
    ST = 0.6  # 预警值
    PD = 0.7  # 发现者的比列，剩下的是加入者
    SD = 0.2  # 意识到有危险麻雀的比重
    PDNumber = int(pop * PD)  # 发现者数量
    SDNumber = int(pop * SD)  # 意识到有危险麻雀数量
    X, lb, ub = initial(pop, dim, ub, lb)  # 初始化种群
    fitness = CaculateFitness(X, fun(X))  # 计算适应度值
    fitness, sortIndex = SortFitness(fitness)  # 对适应度值排序
    X = SortPosition(X, sortIndex)  # 种群排序
    GbestScore = copy.copy(fitness[0])
    GbestPositon = np.zeros([1, dim])
    GbestPositon[0, :] = copy.copy(X[0, :])
    Curve = np.zeros([Max_iter, 1])
    for i in range(Max_iter):

        BestF = fitness[0]

        X = PDUpdate(X, PDNumber, ST, Max_iter, dim)  # 发现者更新

        X = JDUpdate(X, PDNumber, pop, dim)  # 加入者更新

        X = SDUpdate(X, pop, SDNumber, fitness, BestF)  # 危险更新

        X = BorderCheck(X, ub, lb, pop, dim)  # 边界检测

        fitness = CaculateFitness(X, fun(X))  # 计算适应度值
        fitness, sortIndex = SortFitness(fitness)  # 对适应度值排序
        X = SortPosition(X, sortIndex)  # 种群排序
        if (fitness[0] <= GbestScore):  # 更新全局最优
            GbestScore = copy.copy(fitness[0])
            GbestPositon[0, :] = copy.copy(X[0, :])
        Curve[i] = GbestScore

    return GbestScore, GbestPositon, Curve

def fun(x):
    return x[0] ** 2 + x[1] ** 2


if __name__ == '__main__':
    pop = 100
    dim = 2
    lb = 0
    ub = 1
    Max_iter = 1000
    print(SSA(pop, dim, lb, ub, Max_iter))


