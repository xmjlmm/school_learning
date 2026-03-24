'''
# ----------------------- README ------------------------------------------
# -------------- 原创：Seyedali Mirjalili ---------------------------------
# -------------- 最后一次修改：2023/10/6 -----------------------------------
# -------------------  欢迎关注₍^.^₎♡  -------------------------------------
# -------------- 项目：鲸鱼优化算法(WOA)  ----------------------------------
# -------------- 微信公众号：KAU的云实验台 ---------------------------------
# -------------- CSDN:KAU的云实验台 ----------------------------------------
# -------------------------------------------------------------------------
'''

import numpy as np
from matplotlib import pyplot as plt
import math
import random
import copy

''' --------------------------- 预定义子函数 ----------------------------------'''


# 适应度函数F10  返回适应度值
def fun(X):
    dim = X.shape[0]  # 列数
    O = -20 * np.exp(-.2 * np.sqrt(np.sum(X ** 2) / dim)) - np.exp(np.sum(np.cos(2 * np.pi / 180 * X)) / dim) + 20 + np.exp(1)
    return O


# 初始化种群函数  返回初始种群编码
def initialization(popsize, ub, lb, dim):
    X = np.zeros([popsize, dim])
    for i in range(popsize):
        for j in range(dim):
            X[i, j] = (ub[j] - lb[j]) * np.random.random() + lb[j]

    return X


# 越界检查 返回规范后的种群编码
def BorderCheck(X, ub, lb, pop, dim):
    for i in range(pop):
        for j in range(dim):
            if X[i, j] > ub[j]:
                X[i, j] = ub[j]
            elif X[i, j] < lb[j]:
                X[i, j] = lb[j]
    return X


# 计算个体适应度  返回种群适应度
def CaculateFitness(X, fun):
    pop = X.shape[0]  # 个体数
    fitness = np.zeros([pop, 1])
    for i in range(pop):
        fitness[i] = fun(X[i, :])
    return fitness


# 种群排序 返回排序后的适应度和顺序
def SortFitness(Fit):
    fitness = np.sort(Fit, axis=0)
    index = np.argsort(Fit, axis=0)
    return fitness, index


# 根据排序结果对种群位置调整 返回调整后的种群矩阵
def SortPosition(X, index):
    Xnew = np.zeros(X.shape)
    for i in range(X.shape[0]):
        Xnew[i, :] = X[index[i], :]
    return Xnew


''' ---------------------------------------- 定义完成  --------------------------------------------- '''

''' ---------------------------------------- 主函数部分 -------------------------------------------- '''

''' 设置参数 '''
pop = 100 #群数量
MaxIter = 500  # 最大迭代次数
dim = 2 #维度
lb = -32 * np.ones(dim)  # 下边界
ub = 32 * np.ones(dim)  # 上边界

'''初始化种群'''
X = initialization(pop, ub, lb, dim)  # 初始化种群
print(X)
fitness = CaculateFitness(X, fun)  # 计算适应度值
fitness, sortIndex = SortFitness(fitness)  # 对适应度值排序
X = SortPosition(X, sortIndex)  # 种群排序
GbestScore = copy.copy(fitness[0])  # 记录最优适应度值
GbestPositon = np.zeros([1, dim])
GbestPositon[0, :] = copy.copy(X[0, :])  # 记录最优解
Curve = np.zeros([MaxIter, 1])

'''迭代'''
for t in range(MaxIter):

    print('第' + str(t) + '次迭代')
    Leader = X[0, :]  # 领头鲸鱼

    a = 2 - t * (2 / MaxIter)  # 控制参数a
    a2 = -1 + t * ((-1) / MaxIter)

    for i in range(pop):

        # A和C更新
        r1 = random.random()
        r2 = random.random()
        A = 2 * a * r1 - a
        C = 2 * r2

        # b和l更新
        b = 1
        l = (a2-1)*random.random() + 1  # [-1,1]之间的随机数

        for j in range(dim):
            # 随机数p
            p = random.random()
            if p < 0.5:
                if np.abs(A) >= 1:

                    # 搜索觅食机制
                    rand_leader_index = min(int(np.floor(pop * random.random() + 1)),
                                            pop - 1)  # 随机选择一个个体
                    X_rand = X[rand_leader_index, :]
                    D_X_rand = np.abs(C * X_rand[j] - X[i, j])
                    X[i, j] = X_rand[j] - A * D_X_rand

                elif np.abs(A) < 1:

                    # 收缩包围机制
                    D_Leader = np.abs(C * Leader[j] - X[i, j])
                    X[i, j] = Leader[j] - A * D_Leader

            elif p >= 0.5:
                # 螺旋更新位置
                distance2Leader = np.abs(Leader[j] - X[i, j])
                X[i, j] = distance2Leader * np.exp(b * l) * np.cos(l * 2 * math.pi) + Leader[j]

    X = BorderCheck(X, ub, lb, pop, dim)  # 边界检测
    fitness = CaculateFitness(X, fun)  # 计算适应度值
    fitness, sortIndex = SortFitness(fitness)  # 对适应度值排序
    X = SortPosition(X, sortIndex)  # 种群排序
    if fitness[0] <= GbestScore:  # 更新全局最优
        GbestScore = copy.copy(fitness[0])
        GbestPositon[0, :] = copy.copy(X[0, :])
    Curve[t] = GbestScore


print('最优适应度值：', GbestScore)
print('最优解[x1,x2]：', GbestPositon)

# 绘制适应度曲线
plt.figure(1)
plt.plot(Curve, 'r-', linewidth=2)
plt.xlabel('Iteration', fontsize='medium')
plt.ylabel("Fitness", fontsize='medium')
plt.grid()
plt.title('WOA', fontsize='large')
label = ['WOA']
plt.legend(label, loc='upper right')
plt.savefig('./WOA_Python.jpg')
plt.show()

