'''
有一个
NN 的矩阵方格和 N 个棋了，现在需要将 N个棋了按要求放置到知阵方格中。
要求如下:
1.任意两个棋了不能在同一行
2.任意两个棋子不能在同一列
3.任意两个棋子不能在同一对角线上 (下图红色线段都为对角线)
根据以上要求，问N个棋子放置到N*N矩阵方格中有多少种放置方案
例如: 4*4的矩阵方格，4个棋子，有2种放置方案输入描述:
输入一个正整数N (1<N<11)，表示一个NN的矩阵方格和N个棋子数量
输出描述
输出N个棋子按要求放置到N*N的矩阵方格中有多少种放置方案
样例输入:4
样例输出:2
'''

'''n = int(input())
vis = [0 * n for _ in range(n)]
ans = 0

def dfs(x, y, cnt):
    if x == n and y == n:
        if cnt == 0:
            global ans
            ans = ans + 1
        return
    # y轴遍历
    for i in range(n):
        if vis[i] == 0:
            



dfs(0, 0, n)
'''


'''n = int(input(''))
ls = [[0] * n for _ in range(n)]


def dfs(depth):
    if depth == n:
        return
    if ls[x][y] == 1:
        return

    for i in range(n):
        if ls[depth][i] == 0 and sum(ls[depth]) == 0 and sum():
            ls[depth][i] = 1

ans = 0
dfs(0)'''


import numpy as np

def check(mat,row,column):
    # 检查这一列的每个点
    for k in range(N):
        if mat[k][column] == 1:
            return False
    # 检查形似“\”的斜线的每个点
    for i,j in zip(range(row-1,-1,-1),range(column-1,-1,-1)):
        if mat[i][j] == 1:
            return False
    # 检查形似“/”的斜线的每个点
    for i,j in zip(range(row-1,-1,-1),range(column+1,N)):
        if mat[i][j] == 1:
            return False
    return True

def findQueen(mat,row):
    if row > N-1:
        global cnt
        cnt += 1
        print('第{}个解，对应的棋盘如下所示：'.format(cnt))
        print(mat)
        return
    # 一行一行地放皇后
    for column in range(N):
        if check(mat,row,column):
            mat[row][column] = 1
            findQueen(mat,row+1)
            mat[row][column] = 0

N = 8
cnt = 0
mat = np.zeros((N,N),dtype=int)
findQueen(mat,0)
print('{}皇后问题共有{}个解。'.format(N,cnt))

