'''
一个 2D 网格中的 峰值 是指那些 严格大于 其相邻格子(上、下、左、右)的元素。
给你一个 从 0 开始编号 的 m x n 矩阵 mat ，其中任意两个相邻格子的值都 不相同 。找出 任意一个 峰值 mat[i][j] 并 返回其位置 [i,j] 。
你可以假设整个矩阵周边环绕着一圈值为 -1 的格子。
要求必须写出时间复杂度为 O(m log(n)) 或 O(n log(m)) 的算法'''

'''
案例
输入: mat = [[1,4],[3,2]]
输出: [0,1]
解释: 3 和 4 都是峰值，所以[1,0]和[0,1]都是可接受的答案。
输入: mat = [[10,20,15],[21,30,14],[7,16,32]]
输出: [1,1]
解释: 30 和 32 都是峰值，所以[1,1]和[2,2]都是可接受的答案。
'''


def dfs(depth):
    if depth == n + 1:
        global ans
        ans += 1
        print(path)
        return


    for i in range(1, m + 1):
        if vis1[depth] or vis2[i]:
            continue

        path.append([depth - 1, i - 1])
        vis1[depth] = vis2[i] = True
        dfs(depth + 1)
        vis1[depth] = vis2[i] = False
        path.pop()


mat = [[1,4],[3,2]]
n = len(mat)
m = len(mat[0])
path = []
vis1 = [False] * (m + 2)
vis2 = [False] * (m + 2)
ans = 0
dfs(1)
print(ans)
