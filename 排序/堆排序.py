# 编写一个python程序，使用堆排序对数组进行排序

def heapify(arr, n, i):
    largest = i  # 将当前节点设为最大值

    left_child = 2 * i + 1  # 左子节点索引
    right_child = 2 * i + 2  # 右子节点索引

    if left_child < n and arr[i] < arr[left_child]:
        largest = left_child  # 如果左子节点比根节点更大，则更新最大值索引

    if right_child < n and arr[largest] < arr[right_child]:
        largest = right_child  # 如果右子节点比最大值索引对应的元素更大，则更新最大值索引

    if largest != i:  # 若最大值不在正确位置上，交换并递归调用heapify函数
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

# 建立最小堆（从第n/2开始）
def buildHeap(ls):
    n = len(ls)
    for i in range(n // 2 - 1, -1, -1):
        heapify(ls, n, i)

# 进行堆排序
def heapSort(arr):
    buildHeap(arr)  # 构建初始堆
    for i in range(len(arr) - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # 取出最大值放到未排序部分的最后
        heapify(arr, i, 0)  # 重新调整剩余部分成为堆

# 测试样例
if __name__ == "__main__":
    arr = [4, 65, 97, 83, 27, 50]
    print("原始数组：", arr)
    heapSort(arr)
    print("排序结果：", arr)