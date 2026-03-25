import os
import sys

# 请在此输入您的代码
n = 0
for a in range(1, 11):
    for b in range(a, 11):
        for c in range(b, 11):
            for d in range(c, 11):
                for e in range(d, 11):
                    n += 1

print(n)