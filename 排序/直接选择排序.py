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


if __name__ == '__main__':
    ls = [1, 4, 2, 11, 6, 31, 52, 53, 2, 1, 8, 10, 9, 95, 280, 41, 4801, 489, 483, 491]
    ans = selection_list(ls, 0)
    print(ans)