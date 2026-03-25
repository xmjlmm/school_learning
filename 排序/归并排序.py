# 编写一个python程序，使用直接归并排序对数组进行排序
import math
'''

def max_factor(n):
    max = 0
    for i in range(2, int(math.sqrt(n)+1)):
        if n % i == 0:
            max = i
    return max

def merge_sort(ls, public_factor):
    




    return

if __name__ == '__main__':
    ls = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    length = len(ls)
    public_factor = max_factor(length)
    ans = merge_sort(ls, public_factor)
    print(ans)

'''

# def merge_sort(arr):
#     '''
#     归并排序算法实现
#     :param arr: 待排序的数组
#     :return: 排序后的数组
#     '''
#     if len(arr) <= 1:
#         return arr
#
#     mid = len(arr) // 2
#     left = merge_sort(arr[:mid])
#     right = merge_sort(arr[mid:])
#
#     return merge(left, right)
#
# def merge(left, right):
#     '''
#     归并操作，将两个已排序的数组合并成一个已排序的数组
#     :param left: 第一个已排序的数组
#     :param right: 第二个已排序的数组
#     :return: 合并后的已排序的数组
#     '''
#     result = []
#     i = j = 0
#
#     while i < len(left) and j < len(right):
#         if left[i] <= right[j]:
#             result.append(left[i])
#             i += 1
#         else:
#             result.append(right[j])
#             j += 1
#     result.extend(left[i:])
#     result.extend(right[j:])
#     print(result)
#     return result
#
# # 测试样例
# if __name__ == '__main__':
#     array = [54, 26, 93, 17, 77, 31, 44, 55, 20, 10]
#     sorted_array = merge_sort(array)
#     print("Sorted array:", sorted_array)



def merge_sort(arr):
    '''
    归并排序算法实现
    :param arr: 待排序的数组
    :return: 排序后的数组
    '''
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    '''
    归并操作，将两个已排序的数组合并成一个已排序的数组
    :param left: 第一个已排序的数组
    :param right: 第二个已排序的数组
    :return: 合并后的已排序的数组
    '''
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    print(result)
    return result

# 测试样例
if __name__ == '__main__':
    array = [54, 26, 93, 17, 77, 31, 44, 55, 20, 10]
    sorted_array = merge_sort(array)
    print("Sorted array:", sorted_array)
