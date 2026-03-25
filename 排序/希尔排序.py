# 编写一个python程序，使用希尔排序对数组进行排序
import math

# 写一个计算不超过最大元素的最大质数的函数,返回质数间隔列表
def isPrime(ls):
    isprime = [1]
    n = len(ls)
    if n <= 0:
        return -1
    if n >= 2:
        isprime.append(2)
    # 这个偶数怪怪的
    # isprime.append(2)
    for i in range(3, n, 2):
        flag = True
        for j in range(2, int(math.sqrt(i))+1):
            if i % j == 0:
                flag = False
                break
        if flag == True:
            isprime.append(i)
    return isprime

# 将gap逆序输出
def reverse_gap(gap):
    gap_re = []
    for i in range(len(gap)-1, -1, -1):
        gap_re.append(gap[i])
    return gap_re

# 希尔排序主函数
def shell_sort(ls, gap_re):
    for i in range(len(gap_re)):
        gap = gap_re[i]
        for j in range(gap, len(ls)):
            if ls[j] < ls[j-gap]:
                ls[j], ls[j-gap] = ls[j-gap], ls[j]
    return ls

# 主函数部分调用希尔排序
if __name__ == '__main__':
    ls = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    gap = isPrime(ls)
    gap_re = reverse_gap(gap)
    ans = shell_sort(ls, gap_re)
    print(gap)
    print(gap_re)
    print(ans)