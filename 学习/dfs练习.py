'''
两种糖果分别有9个和16个，要全部分给7个小朋友，每个小朋友得到的糖果总数最少为2个最多为5个，
问有多少种不同的分法。糖果必须全部分完。
只要有其中一个小朋友在两种方案中分到的糖果不完全相同，这两种方案就算作不同的方案
'''


'''def dfs(depth):
    if depth == 7:
        suma = 0
        sumb = 0
        for a, b in path:
            suma += a
            sumb += b
        if suma == 9 and sumb == 16:
            global ans
            ans += 1
        return


    for i in range(0,7):
        for j in range(0,7):
            if 2 <= i + j <= 5:
                path.append([i,j])
                dfs(depth + 1)
                path.pop()

ans = 0
path = []
dfs(0)
print(ans)'''


'''
def dfs(depth, suma, sumb):
    if depth == 7:
        #可行性剪枝
        if suma > 9 or sumb > 16:
            return
        if suma == 9 and sumb == 16:
            global ans
            ans += 1
        return


    for i in range(0, 6):
        for j in range(0, 6):
            if 2 <= i + j <= 5:
                # path.append([i,j])
                dfs(depth + 1, suma +i, sumb + j)
                # path.pop()

ans = 0
# path = []
dfs(0, 0, 0)
print(ans)

'''



'''def dfs(depth, suma, sumb):
    if depth == 7:
        if suma == 0 and sumb == 0:
            global ans
            ans += 1
        return

    for i in range(0, 6):
        for j in range(0, 6 - i):
            if 2 <= i + j <= 5:
                dfs(depth + 1, suma - i, sumb - j)

ans = 0
dfs(0, 9, 16)
print(ans)'''



'''def dfs(depth, suma, sumb):
    if depth == 7:
        # 可行性剪枝
        if suma > 9 or sumb > 16:
            return

        # 最优性剪枝
        if 25 - suma - sumb < 2 * (7 - depth) or 25 - suma -sumb > 5 * (7 - depth):
            return
        if suma == 9 and sumb == 16:
            global ans
            ans += 1
        return


    for i in range(0, 6):
        for j in range(0, 6 - i):
            if 2 <= i + j <= 5:
                # path.append([i,j])
                dfs(depth + 1, suma + i, sumb + j)
                # path.pop()

ans = 0
# path = []
dfs(0, 0, 0)
print(ans)'''

import sys
sys.setrecursionlimit(100000000)

ans = 0
def dfs(depth, candle1, candle2):
    global ans
    # 判断结束条件
    if depth == 7:
        if candle1 == 0 and candle2 == 0:
            ans = ans + 1
        return

    for i in range(6):
        for j in range(6-i):
            sum_candle = i + j
            if sum_candle <= 5 and sum_candle >= 2:
                dfs(depth + 1, candle1 - i, candle2 - j)
dfs(0, 9, 16)
print(ans)


'''ans = 0
def dfs(depth, n, m):
    global ans
    if depth == 7:
        if n == 0 and m == 0:
            ans += 1
        return
    for i in range(n + 1):
        for j in range(m + 1):
            if 2 <= i + j <= 5 and i <= n and j <= m:
                dfs(depth + 1, n - i, m - j)
dfs(0,9,16)
print(ans)'''