# 编写一个python程序，使用冒泡排序对数组进行排序

def bubble_sort(ls):
    length = len(ls)
    for i in range(1, length):
        # 如果在一次循环中没有元素进行位次交换，说明数组已经有序，可以提前结束排序
        flag = 0
        for j in range(0, length - i):
            if ls[j] > ls[j + 1]:
                flag = 1
                ls[j], ls[j + 1] = ls[j + 1], ls[j]
        if flag == 0:
            break
    return ls

if __name__ == '__main__':
    ls = [1, 4, 2, 11, 6, 31, 52, 53, 2, 1, 8, 10, 9, 95, 280, 41, 4801, 489, 483, 491]
    ans = bubble_sort(ls)
    print(ans)