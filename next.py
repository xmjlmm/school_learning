my_list = [1, 2, 3]
it = iter(my_list)  # 创建迭代器对象

print(next(it))  # 输出1
print(next(it))  # 输出2
print(next(it))  # 输出3


my_list = [1, 2, 3]
it = iter(my_list)

try:
    print(next(it))  # 输出1
    print(next(it))  # 输出2
    print(next(it))  # 输出3
    print(next(it))  # 没有更多元素，引发StopIteration异常
except StopIteration:
    print("迭代器中没有更多元素")

