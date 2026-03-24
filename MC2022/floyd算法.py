import numpy as np
from numpy import inf
A = [[inf, 3, inf,2, inf],
   [3, inf, 2, 1, inf],
   [inf, 2,inf, inf, 5],
   [2, 1, inf, inf, 4],
   [inf, inf, 5, 4, inf]]
n = len(A[0])
dis = A # 邻接矩阵包含了任意两个节点之间的距离，distance
path = np.zeros((n, n)) # 初始化路由矩阵，让它都是零
for k in range(n):
    for i in range(n):
        for j in range(n):
            if dis[i][k]+dis[k][j]<dis[i][j]:
                dis[i][j]=dis[i][k]+dis[j][k] # 找到经过k点时路径更短，接受这个更短的路径长度
                path[i][j]=k # 路由矩阵记录路径
print(dis) # 显示每对顶点最短路径长度
print(path) # 显示路由矩阵