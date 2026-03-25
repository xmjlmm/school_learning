'''8465:马走日
马在中国象棋以日字形规则移动。
请编写一段程序，给定 n*m
大小的棋盘，以及马的初始位置 (x，y) ，
要求不能重复经过棋盘上的同一个点，计算马可以有多少途径遍历棋盘上的所有点。
输入
第一行为整数 T (T < 10)表示测试数据组数。
每一组测试数据包含一行，为四个整数，分别为棋盘的大小以及初始位置坐标n,m,x,y(0<x<m-1, 0<y<n-1, m<10, n<10)
输出
每组测试数据包含一行，为一个整数，表示马能遍历棋盘的途径总数， 0 为无法遍历一次。
样例输入
1
5400
样例输出
32
'''
'''
T = int(input(''))
st = input('')
n = int(st.split(' ')[0])
m = int(st.split(' ')[1])
x = int(st.split(' ')[2])
y = int(st.split(' ')[3])
ls = [[0] * m for i in range(n)]

def dfs(x, y):
    if x < 0 or x >= n:
        return
    if y < 0 or y >= m:
        return
    if ls[x][y] == 1:
        return

    ls[x][y] = 1
    
    dfs(x+2, y+1)
    dfs(x-2, y-1)
    dfs(x+1, y+2)
    dfs(x-1, y-2)
    dfs(x-2, y+1)
    dfs(x+2, y-1)
    dfs(x+1, y-2)
    dfs(x-1, y+2)

ans = 0

for i in range(x, -1, -1):
    for j in range(y, -1, -1):
        if ls[i][j] == 0:
            dfs(i, j)
            ans = ans + 1

for i in range(x, n, 1):
    for j in range(y, m, 1):
        if ls[i][j] == 0:
            dfs(i, j)
            ans = ans + 1

print(ans)
'''



T = int(input(''))
for _ in range(T):
    st = input('')
    n = int(st.split(' ')[0])
    m = int(st.split(' ')[1])
    x = int(st.split(' ')[2])
    y = int(st.split(' ')[3])
    ls = [[0] * n for i in range(m)]
    dirs = [(1, 2), (2, 1), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1),]
    ans = 0

    def dfs(x, y, step):
        global ans
        if step == n * m:
            ans = ans + 1
            return

        for length in range(8):
            next_x = dirs[length][0] + x
            next_y = dirs[length][1] + y
            if next_x >= 0 and next_x <= m-1 and next_y <= n-1 and next_y >= 0 and ls[next_x][next_y] == 0:
                ls[next_x][next_y] = 1
                dfs(next_x, next_y, step + 1)
                ls[next_x][next_y] = 0

    ls[x][y] = 1
    dfs(x, y, 1)
    print(ans)


