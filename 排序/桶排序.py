# n个数据,m个桶,

def bucket_sort(arr, bucketSize=5):
    if len(arr) == 0:
        return arr

    # 找到最小和最大值
    minValue = arr[0]
    maxValue = arr[0]
    for i in range(1, len(arr)):
        if arr[i] < minValue:
            minValue = arr[i]
        elif arr[i] > maxValue:
            maxValue = arr[i]

    # 初始化桶
    bucketCount = (maxValue - minValue) // bucketSize + 1
    buckets = []
    for i in range(bucketCount):
        buckets.append([])

    # 分配元素到各个桶
    for i in range(len(arr)):
        buckets[(arr[i] - minValue) // bucketSize].append(arr[i])

    # 对每个桶进行排序，这里使用了Python内置的排序
    arr.clear()
    for i in range(len(buckets)):
        buckets[i].sort()
        arr.extend(buckets[i])

    return arr

def main():
    arr = [4, 2, 2, 8, 3, 3, 1]
    print("原始数组:", arr)
    sorted_arr = bucket_sort(arr, bucketSize=2)
    print("排序后的数组:", sorted_arr)

if __name__ == "__main__":
    main()