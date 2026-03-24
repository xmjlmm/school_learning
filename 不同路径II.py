'''
obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
obstacleGrid = [[0,1],[0,0],[0,0]]
obstacleGrid = [[0, 0], [0, 0], [1, 0]]
m = len(obstacleGrid)
n = len(obstacleGrid[0])

def dfs(i, j):
    if i == m - 1 and j == n - 1 and obstacleGrid[i][j] == 1:
        global ans
        ans = ans + 1
        return
    if i < m - 1 and obstacleGrid[i + 1][j] == 0:
        obstacleGrid[i + 1][j] = 1
        dfs(i + 1, j)
        obstacleGrid[i + 1][j] = 0
    if j < n - 1 and obstacleGrid[i][j + 1] == 0:
        obstacleGrid[i][j + 1] = 1
        dfs(i, j + 1)
        obstacleGrid[i][j + 1] = 0

if __name__ == '__main__':
    ans = 0
    dfs(0, 0)
    print(ans)
'''
'''
class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m, n = len(obstacleGrid), len(obstacleGrid[0])
        dp = [[-1] * n for _ in range(m)]
        # 起点标记为1
        dp[0][0] = 1
        for i in range(m):
            for j in range(n):
                # 标记障碍物，标记为0
                if obstacleGrid[i][j] == 1:
                    dp[i][j] = 0
                    continue
                # 起点
                if i == j == 0:
                    continue
                # 第一行的操作，dp的第一行全为1
                if i == 0:
                    dp[i][j] = dp[i][j-1]
                # 第一列的操作，dp的第一列全为1
                elif j == 0:
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = dp[i-1][j] + dp[i][j-1]
        return dp[m-1][n-1]
'''

obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
m = len(obstacleGrid)
n = len(obstacleGrid[0])
dp = [[-1] * n for _ in range(m)]
dp[0][0] = 1
for i in range(m):
    for j in range(n):
        if obstacleGrid[i][j] == 1:
            dp[i][j] = 0
            continue
        if i == 0 and j == 0:
            continue
        if i == 0 and j > 0:
            dp[i][j] = dp[i][j-1]
        elif j == 0 and i > 0:
            dp[i][j] = dp[i-1][j]
        else:
            dp[i][j] = dp[i][j-1] + dp[i-1][j]
print(dp[m-1][n-1])

