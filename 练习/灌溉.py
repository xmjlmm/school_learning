n, m = map(int, input().split(" "))
t = int(input())
data = [[0] * m for _ in range(n)]  # n行m列的花园，0代表未灌溉
flag = [[0] * m for _ in range(n)]  # 标记矩阵，标记方格是否访问
stack = []  # 用栈来代替递归栈
for i in range(t):
    x = list(map(int, input().split(" ")))
    data[x[0] - 1][x[1] - 1] = 1  # 初始化出水管位置，1代表已灌溉
    stack.append([x[0] - 1, x[1] - 1])  # 将出水管位置入栈
k = int(input())
ans = 0
while k >= 0 and stack:  # 若栈不为空或时间大于等于0则循环
    st = []  # 保存下一次循环元素的栈
    while stack:  # 遍历所有栈元素，每个元素尝试向四周扩展并将新元素加入新栈
        grid = stack.pop()
        flag[grid[0]][grid[1]] = 1
        ans += 1  # 答案加一
        if grid[0] > 0 and flag[grid[0] - 1][grid[1]] == 0:
            st.append([grid[0] - 1, grid[1]])
        if grid[0] < n - 1 and flag[grid[0] + 1][grid[1]] == 0:
            st.append([grid[0] + 1, grid[1]])
        if grid[1] > 0 and flag[grid[0]][grid[1] - 1] == 0:
            st.append([grid[0], grid[1] - 1])
        if grid[1] < m - 1 and flag[grid[0]][grid[1] + 1] == 0:
            st.append([grid[0], grid[1] + 1])
    k -= 1  # 遍历完一次栈表示所有点已扩展完一次，时间减一
    stack = st[::]  # 更新栈为下一次的栈元素

print(ans)