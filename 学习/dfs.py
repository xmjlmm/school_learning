'''

def dfs(depth):
    if depth == n:
        global cnt
        cnt += 1
        #可修改的条件判断
        flag = True
        for i in range(len(path)-1):
            if path[i] > path[i+1]:
                flag = False
                break
        if flag and sum(path) == x:
            print(path)
        return
    for i in range(1, x + 1):
        path.append(i)
        dfs(depth + 1)
        path.pop()


x = int(input('x:'))
n = int(input('n:'))
cnt = 0
path = []
dfs(0)
print(cnt)
'''

# -----------------------------------------------------------------

'''
def dfs(depth, last_val):
    if depth == n:
        global cnt
        cnt += 1
        if sum(path) == x:
            print(path)
        return

    for i in range(last_val, x+1):
        path.append(i)
        dfs(depth+1, i)
        path.pop()

x = int(input('x:'))
n = int(input('n:'))
path = []
cnt = 0
dfs(0, 1)
print(cnt)
'''

# -----------------------------------------------------------------

'''
# 模板一：
def dfs(depth):
    '''
    #: param depth: 当前为第几重循环
    #: return:
    '''
    # 第0重 - 第n-1重都已经选好数字，此时只需要判断答案
    if depth == n:
        # 条件一： 数字需要递增
        for i in range(1, n):
            if a[i] >= a[i - 1]:
                continue
            else:
                return
        # 条件二：数字和为x
        if sum(a) != x:
            return
        print(a)
        return

    # 第depth层进行
    for i in range(1, x + 1):
        # 选择第depth层的数字
        a[depth] = i
        #递归进入下一层
        dfs(depth + 1)
'''

# -----------------------------------------------------------------

'''
# 模板二
def dfs(depthm last_val):
    '''
    #: param depth: 当前为第几重循环
    #: return:
    '''
    # 第0重 - 第n-1重都已经选好数字，此时只需要判断答案
    if depth == n:
        # 条件二： 数字和为x
        if sum(a) != x:
            return
        #此时是答案
        print(a)
        return
    # 第depth层进行选择数字：[1, x]进行枚举
    #条件一：数字需要递增
    for i in range(last_val, x + 1):
        # 选择第depth层的数字
        a[depth] = i
        # 递归进入下一层
        dfs(depth + 1)
'''

'''
两种糖果分别有9个和16个，要全部分给7个小朋友，每个小朋友得到的糖果总数最少为2个最多为5个，
问有多少种不同的分法。糖果必须全部分完。
只要有其中一个小朋友在两种方案中分到的糖果不完全相同，这两种方案就算作不同的方案
'''


def dfs(depth):
    if depth == n:
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
print(ans)