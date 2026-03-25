import os
import sys
sys.setrecursionlimit(100000) # 递归深度,设置为100000
# 请在此输入您的代码
'''
# 使用dfs深度搜索求解,当n过大，出现段错误
n = int(input(''))
ls = [[] for _ in range(n)]
for i in range(n):
    s = input('')
    s = s.split(' ')
    for k in range(len(s)):
        s[k] = int(s[k])
    ls[i] = s

# depth表示深度,j表示当前要选择的数字,ans表示当前的答案
def dfs(depth, j, ans):
    if depth == n:
        return ans
    tem = ls[depth]
    length = len(tem)
    tem1, tem2, tem3 = 0, 0, 0
    tem1 = dfs(depth + 1, j, ans + tem[j])
    if j + 1 < length:
        tem2 = dfs(depth + 1, j + 1, ans + tem[j + 1])
    ans = max(tem1, tem2)
    return ans

print(dfs(0, 0, 0))
'''

# 使用dp动态规划进行求解,还是出现段错误
'''n = int(input(''))
ls = [[] for _ in range(n)]
for i in range(n):
    s = input('')
    s = s.split(' ')
    for k in range(len(s)):
        s[k] = int(s[k])
    ls[i] = s

dp = [[0] * n for _ in range(n)]
dp[0][0] = ls[0][0]
# 对层进行遍历
for i in range(0, n):
    tep = ls[i]
    length = len(tep)
    # 对每一层的元素进行遍历
    for j in range(0, length):
        if i == 0 and j == 0:
            continue
        if j == 0:
            dp[i][j] = dp[i-1][j] + tep[j]
        elif j == length - 1:
            dp[i][j] = dp[i-1][j-1] + tep[j]
        else:
            dp[i][j] = max(dp[i-1][j] + tep[j], dp[i-1][j-1] + tep[j])
print(dp)
print(max(dp[-1]))'''


'''
# 使用dp动态规划进行求解,还是出现段错误
n = int(input(''))
ls = [[] for _ in range(n)]
for i in range(n):
    s = input('')
    s = s.split(' ')
    for k in range(len(s)):
        s[k] = int(s[k])
    ls[i] = s

# 对层进行遍历
for i in range(0, n):
    tep = ls[i]
    length = len(tep)
    # 对每一层的元素进行遍历
    for j in range(0, length):
        if i == 0 and j == 0:
            continue
        if j == 0:
            ls[i][j] = ls[i-1][j] + tep[j]
        elif j == length - 1:
            ls[i][j] = ls[i-1][j-1] + tep[j]
        else:
            ls[i][j] = max(ls[i-1][j] + tep[j], ls[i-1][j-1] + tep[j])
print(max(ls[-1]))
'''

'''n = int(input(''))
ls = [[] for _ in range(n)]
for i in range(n):
    s = list(map(int, input().split()))
    ls[i] = s

# 对层进行遍历
dp = [[0] * n for _ in range(n)]
dp[0][0] = ls[0][0]
# 对层进行遍历
for i in range(0, n):
    tep = ls[i]
    length = len(tep)
    # 对每一层的元素进行遍历
    for j in range(0, length):
        if i == 0 and j == 0:
            continue
        if j == 0:
            dp[i][j] = dp[i-1][j] + tep[j]
        elif j == length - 1:
            dp[i][j] = dp[i-1][j-1] + tep[j]
        else:
            dp[i][j] = max(dp[i-1][j] + tep[j], dp[i-1][j-1] + tep[j])

print(max(dp[-1]))'''

n = int(input())
tri = []
for _ in range(n):
    ls = list(map(int, input().split()))
    tri.append(ls)

dp = [[0] * (n + 1) for _ in range(n + 1)]
dp[0][0] = 0
# 第一层就是tri的第一个元素
dp[1][0] = tri[0][0]
for i in range(2, n + 1):
    for j in range(0, i):
        if j == 0:
            dp[i][j] = dp[i - 1][j] + tri[i - 1][0]
        elif j == i - 1:
            dp[i][j] = dp[i - 1][j - 1] + tri[i - 1][-1]
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - 1]) + tri[i - 1][j]

if n % 2 != 0:
    locate = int(n//2)
    ans = dp[-1][locate]
else:
    mid = int(n // 2)
    ans = max(dp[n][int(mid)], dp[n][int(mid)-1])

print(ans)