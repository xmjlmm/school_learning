
ls = [[1, 1, 3],
      [2, 3, 4],
      [1, 0, 1]]

n = len(ls)
m = len(ls[0])

def dfs(i, j, val):
    if i < 0 or i == n:
        return 0
    if j < 0 or j == m:
        return 0
    if ls[i][j] >= val:
        return 0

    res = 1
    res = max(res, 1 + dfs(i - 1, j, ls[i][j]))
    res = max(res, 1 + dfs(i + 1, j, ls[i][j]))
    res = max(res, 1 + dfs(i, j - 1, ls[i][j]))
    res = max(res, 1 + dfs(i, j + 1, ls[i][j]))

    return res


dict = {}

for i in range(n):
    for j in range(m):
        ans = dfs(i, j, 100)
        dict[(i, j)] = ans
#print(dict)
print(max(dict.values()))


