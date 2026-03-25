'''1. 在关键字有序序列中采用折半查找法查找关键字为给定值k的元素，输出查找结果。
    要求:有序序列和给定值k都从键盘输入。'''

def first_find_binary_search(arr, key):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < key:
            low = mid + 1
        elif arr[mid] > key:
            high = mid - 1
        else:
            # 找到关键字相等的元素后，向前搜索，找到第一次出现的位置
            while mid > 0 and arr[mid - 1] == key:
                mid -= 1
            return mid
    return -1

def last_find_binary_search(arr, key):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < key:
            low = mid + 1
        elif arr[mid] > key:
            high = mid - 1
        else:
            # 找到关键字相等的元素后，向前搜索，找到第一次出现的位置
            while mid > 0 and arr[mid + 1] == key:
                mid += 1
            return mid
    return -1

def main():
    arr = list(map(int, input("请输入有序序列，以空格分隔: ").split()))
    key = int(input("请输入要查找的关键字: "))
    first_find_result = first_find_binary_search(arr, key)
    last_find_result = last_find_binary_search(arr, key)
    if first_find_result != -1:
        print("关键字 %d 第一次出现的位置是: %d" % (key, first_find_result))
    else:
        print("关键字 %d 未找到" % key)
    if last_find_result != -1:
        print("关键字 %d 最后一次出现的位置是: %d" % (key, last_find_result))
    else:
        print("关键字 %d 未找到" % key)

if __name__ == "__main__":
    main()
