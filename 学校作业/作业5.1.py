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

# 编写一个python程序，使用直接选择排序对数组进行排序
# 将后面的最小值往前放，使用递归完成算法
import math

def selection_list(ls, i):
    length = len(ls)
    if i == length - 1:
        return ls
    min_value = math.inf
    for j in range(i+1, length):
        if ls[j] < min_value:
            min_value = ls[j]
            min_index = j
    if ls[i] > min_value:
        ls[i], ls[min_index] = ls[min_index], ls[i]
    return selection_list(ls, i+1)

# 编写一个python程序，使用快速排序对数组进行排序
import sys
sys.setrecursionlimit(100000) # 递归深度,设置为100000

# 快速排序函数
def quick_sort(ls):
    mini, maxi = [], []
    if len(ls) <= 1:
        return ls
    # 从最后一个元素开始当作主元结点
    pivot = ls.pop()
    for i in range(len(ls)):
        if ls[i] < pivot:
            mini.append(ls[i])
        else:
            maxi.append(ls[i])
    # 返回将主元结点排好序的列表
    return quick_sort(mini) + [pivot] + quick_sort(maxi)

# 主函数部分调用希尔排序
if __name__ == '__main__':
    ls = [54, 26, 93, 17, 77, 31, 44, 55, 20, 16]
    gap = isPrime(ls)
    gap_re = reverse_gap(gap)
    ans1 = shell_sort(ls, gap_re)
    print('希尔排序的排序结果：', ans1)
    ans2 = selection_list(ls, 0)
    print('直接选择排序的排序结果：', ans2)
    ans3 = quick_sort(ls)
    print('直接快速排序：', ans3)
