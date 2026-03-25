import sys
sys.setrecursionlimit(100000) # 递归深度,设置为100000
# 编写Python代码，实现顺序表的二分查找操作。

def biList(ls, key):
    # 非递归二分查找
    left = 0
    right = len(ls) - 1
    while left < right:
        mid = (left + right) // 2
        if ls[mid] == key:
            return mid
        elif ls[mid] > key:
            right = mid - 1
        else:
            left = mid + 1
    return -1

def regList(ls, key, left, right):
    # 递归二分查找
    if left > right:
        return -1
    mid = (left + right) // 2
    if ls[mid] == key:
        return mid
    elif ls[mid] < key:
        return regList(ls, key, mid + 1, right)
    else:
        return regList(ls, key, left, mid - 1)

ls = [1, 4, 2, 11, 6, 31, 52, 53, 2, 1, 8, 10, 9, 95, 280, 41, 4801, 489, 483, 491]
ls.sort()
print(ls)
key = int(input('请输入要查找的元素为：'))
ans = biList(ls, key)
left, right = 0, len(ls) - 1
res = regList(ls, key, left, right)
print(ans)
print(res)
