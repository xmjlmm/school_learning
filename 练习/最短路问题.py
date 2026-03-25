import os
import sys
import math

# 请在此输入您的代码

s = input('')
s = s.split(' ')
n = int(s[0])
q = int(s[1])


# 定义非素数是0, 素数是1, 1既不是素数也不是合数
def isPrime(n):
    if n == 1:
        return 0
    if n == 2:
        return 1
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            return 0
    return 1


def gcd(a, b):
    # 将a, b中较大的数放在b中
    if a > b:
        a, b = b, a
    c = b % a
    while c:
        b = a
        a = c
        c = b % a
    return a

def pcd(a, b, c):
    return a * b // c

def main(a, b):
    if a >= b or a < 1 or b > n:
        return -1
    if isPrime(a) + isPrime(b) != 1:
        return -1
    tem = gcd(a, b)
    ans = pcd(a, b, tem)
    return ans

for j in range(q):
    s1 = input('')
    s1 = s1.split(' ')
    a = int(s1[0])
    b = int(s1[1])
    ans = -1
    print(main(a, b))


