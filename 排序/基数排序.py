# 编写一个python程序，使用基数排序对数组进行排序

def radix_sort(arr):
    # 获取最大值并计算位数
    max_val = max(arr)
    digits = len(str(max_val))

    for i in range(digits - 1, -1, -1):
        count = [0] * (len(arr) + 1)  # 创建计数器列表

        # 统计每个元素在当前位上的频次
        for num in arr:
            # 计算第i位上的数字
            digit = int((num // (10 ** i))) % 10
            count[digit + 1] += 1

        # 根据频次重新分配元素到正确的位置
        for j in range(2, len(count)):
            count[j] += count[j - 1]

        output = [None] * len(arr)
        for k in reversed(range(len(arr))):
            digit = int((arr[k] // (10 ** i))) % 10
            output[count[digit]] = arr[k]
            count[digit] -= 1

    return output

# 测试样例
if __name__ == '__main__':
    array = [543, 678, 901, 234, 123, 456]
    sorted_array = radix_sort(array)
    print("Sorted array:", sorted_array)