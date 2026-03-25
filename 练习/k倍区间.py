'''
hash = []
init_ls = []
ans = 0
n, k = map(int, input().split())
for _ in range(n):
    ele = int(input())
    init_ls.append(ele)

for i in range(1, n+1):
    for j in range(n-i+1):
        sum_num = sum(init_ls[j:j+i])
        hash.append(sum_num)
for m in hash:
    if m % k == 0:
        ans = ans + 1
print(ans)
'''


# 前缀和的思想















