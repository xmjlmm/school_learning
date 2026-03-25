import os
import sys

# 请在此输入您的代码

def max_len(ls):
    # 从最大的边长开始遍历
    for edge in range(max(max(ls)), 0, -1):
        # 统计能切割出的正方形巧克力块数
        count = 0
        for num in ls:
            a = num[0] // edge
            b = num[0] // edge
            count = count + a * b
        if count >= k:
            return edge

n, k = map(int, input().split())
ls = [[] for _ in range(n)]
for i in range(n):
    s = list(map(int, input().split()))
    ls[i] = s
print(max_len(ls))