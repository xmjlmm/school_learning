# 重量 1 2 4 2 5
# 价值 5 3 5 3 2
# 重量限制10kgs
''' 不带备忘录的0-1规划
W = [0, 1, 2, 4, 2, 5]
V = [0, 5, 3, 5, 3, 2]

def ks(n, C):
    if n == 0 or C == 0:
        result = 0
    elif W[n] > C:
        result = ks(n - 1, C)
    else:
        tmp1 = ks(n - 1, C)
        tmp2 = V[n] + ks(n - 1, C - W[n])
        result = max(tmp1, tmp2)
    return result

n = int(input('n:'))
C = int(input('C:'))

ans = ks(n, C)
print(ans)
'''

'''
带备忘录的0-1规划
W = [0, 1, 2, 4, 2, 5]
V = [0, 5, 3, 5, 3, 2]

def ks(n, C):
    if memo[n][C] != 0:
        for ele in memo:
            print(ele)
    if n == 0 or C == 0:
        result = 0

    elif W[n] > C:
        result = ks(n - 1, C)
    else:
        tmp1 = ks(n - 1, C)
        tmp2 = V[n] + ks(n - 1, C - W[n])
        result = max(tmp1, tmp2)
    memo[n][C] = result
    return result


n = int(input('n:'))
C = int(input('C:'))
memo = [[0] * (C + 1) for _ in range(n + 1)]
res = ks(n, C)
print(res)
'''

'''编程实现:
期末考试小明取得了优异的成绩，妈妈为鼓励小明再接再厉，在网购平台指定了N ( 2<=N<=50)件礼物供小明挑选，挑选前妈妈提出了以下要求:
1)每种礼物只能挑选1件 ;
2)所挑选的礼物总价格不能大于V(1<=V<=100)。
已知N件礼物中每件礼物的价格和小明对每件礼物的喜爱值(喜爱值越大喜爱程度越高 ) ，
请你帮助小明挑选礼物，使得挑选的所有礼物在满足要求的前提下，总的喜爱值最大，并输出最大喜爱值·
例如:
N=3，V=53件礼物的价格和喜爱值分别为(1“2)， (2·4)，(33)。
可挑选第二件礼物(2，4)和第三件礼物(3，3)，总价格为5(52+3)，总喜爱值为7(7=4+3)，总价格不大于5且喜爱值最大，输出7
输入描述
第一行输入两个正整数N(2<=N<=50) 和V(1<=V<=100)，分别表示指定的礼物数量和所挑选的礼物总价格不能大于的值，正整数之间以一个英文逗号隔开
第二行开始，输入N行，每行输人两个正整数J(1<=J<=V) 和K(K<100)，分别表示每件礼物的价格和喜爱值，正整数之间以一个英文逗号隔开
输出描述
输出一个整数，表示在满足题目要求下的最大喜爱值
'''
'''
init = input('')
N = int(init.split(',')[0])
V = int(init.split(',')[1])
E = [0]
P = [0]
for i in range(N):
    val = input('')
    P.append(int(val.split(',')[0]))
    E.append(int(val.split(',')[1]))



def ks(N, V):
    if N == 0 or V == 0:
        result = 0
    elif P[N] > V:
        result = ks(N - 1, V)
    else:
        tmp1 = ks(N - 1, V)
        tmp2 = ks(N - 1, V - P[N]) + E[N]
        result = max(tmp1, tmp2)

    return result

ans = ks(N, V)
print(ans)
'''

'''
init = input('')
N = int(init.split(',')[0])
V = int(init.split(',')[1])
E = [0]
P = [0]
for i in range(N):
    val = input('')
    P.append(int(val.split(',')[0]))
    E.append(int(val.split(',')[1]))

def ks(N, V):
    if memo[N][V] != 0:
        for ele in memo:
            print(ele)
    if N == 0 or V == 0:
        result = 0
    elif P[N] > V:
        result = ks(N - 1, V)
    else:
        tmp1 = ks(N - 1, V)
        tmp2 = ks(N - 1, V - P[N]) + E[N]
        result = max(tmp1, tmp2)

    memo[N][V] = result

    return result

memo = [[0] * (V + 1) for _ in range(N + 1)]
ans = ks(N, V)
print(ans)
'''
# import random
# print(random.randint(1, 10)+random.random())

import os
import sys

# 请在此输入您的代码

s = input('')
s = s.split(' ')
total_weight = int(s[0])
n = int(s[1])
W, V = [], []
for i in range(n):
    s = input('')
    s = s.split(' ')
    W.append(int(s[0]))
    V.append(int(s[1]))

def dfs(total_weight, depth):
    if depth == n or total_weight <= 0:
        result = 0
    elif total_weight < W[depth]:
        result = dfs(total_weight, depth + 1)
    else:
        temp1 = dfs(total_weight - W[depth], depth+1) + V[depth]
        temp2 = dfs(total_weight, depth+1)
        result = max(temp1, temp2)
    return result

ans = 0
ans = dfs(total_weight, 0)
print(ans)


s = input('')
s = s.split(' ')
total_weight = int(s[0])
n = int(s[1])
W, V = [], []
for i in range(n):
    s = input('')
    s = s.split(' ')
    W.append(int(s[0]))
    V.append(int(s[1]))

def dfs(total_weight, depth):
    if depth == n or total_weight <= 0:
        ans = 0
    elif total_weight < W[depth]:
        ans = dfs(total_weight, depth + 1)
    else:
        temp1 = dfs(total_weight, depth + 1)
        temp2 = dfs(total_weight - W[depth], depth + 1) + V[depth]
        ans = max(temp1, temp2)
    return ans

dp = [0] for _ in range(total_weight + 1)
ans = 0
dfs(total_weight, 0)
print(ans)