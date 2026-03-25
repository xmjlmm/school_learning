# import threading
# import time
#
# # 睡眠排序算法
# def sleep_sort(numbers):
#     def sleep_and_print(number):
#         time.sleep(number)
#         print(number)
#
#     for number in numbers:
#         # 创建一个新线程，让其在number秒后输出
#         thread = threading.Thread(target=sleep_and_print, args=[number])
#         thread.start()
#
#
# numbers = [2,3,4,5,6,7,8,2,4,5,6]
# sleep_sort(numbers)


import time
import threading

def sleep_sort(values):
    result = []

    # 定义一个函数，用于"睡眠"后添加数字到结果列表
    def place_number(num):
        time.sleep(num)  # 睡眠时间按数值大小决定
        result.append(num)
        print(num, end=' ')

    # 为每个数启动一个线程
    threads = []
    for number in values:
        thread = threading.Thread(target=place_number, args=(number,))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    return result

# 示例用法
if __name__ == "__main__":
    nums = [4, 1, 3, 2, 0.5, 5, 777, 56, 45]
    print("Sorted numbers:")
    sorted_nums = sleep_sort(nums)
    print(sorted_nums)