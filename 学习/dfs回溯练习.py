'''
在N x N的方格棋盘放置了N个皇后，使得它们不相互攻击
（即任意2个皇后不允许处在同一排，同一列，也不允许处在与棋盘边框成45角的斜线上。
你的任务是，对于给定的N，求出有多少种合法的放置方法。
'''

def dfs(depth):
    if depth == n + 1:
        print(path)
        global ans
        ans += 1
        return

    for i in range(1, n + 1):
        if vis[i] or vis1[depth + i] or vis2[depth - i + n]:
            continue

        path.append(i)
        vis[i] = vis1[i + depth] = vis2[depth - i + n] = True
        dfs(depth + 1)
        vis[i] = vis1[depth + i] = vis2[depth - i + n] = False
        path.pop()

n = int(input('n:'))
ans = 0
path = []
vis = [False] * (n + 1)
vis1 = [False] * (2 * n + 1)
vis2 = [False] * (2 * n + 1)
dfs(1)
print(ans)

