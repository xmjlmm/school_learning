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

# 主函数部分调用快速排序
if __name__ == '__main__':
    ls = [54, 26, 93, 17, 77, 31, 44, 55, 20]
    ans = quick_sort(ls)
    print(ans)