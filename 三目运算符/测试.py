num = 10
result = "偶数" if num % 2 == 0 else "奇数"
print(result)  # 输出: "偶数"
print('###############################################################')

num = -5
absolute_value = num if num >= 0 else -num
print(absolute_value)  # 输出: 5
print('###############################################################')

numbers = [1, -2, 3, -4, 5]
numbers = [x if x >= 0 else 0 for x in numbers]
print(numbers)  # 输出: [1, 0, 3, 0, 5]
print('###############################################################')

num = -7
result = "正数" if num > 0 else ("零" if num == 0 else "负数")
print(result)  # 输出: "负数"
print('###############################################################')


nums = [1, 2, 3, 4, 56, 8]
first = 5
result = [first if first >= nums[i] else nums[i] for i in range(1, (length := len(nums)))]
print(result)  # 输出: [5, 5, 5, 56, 8]