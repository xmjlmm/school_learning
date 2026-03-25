numbers1 = [1, 2, 3, 4, 5]
numbers2 = [10, 20, 30, 40, 50]
sum_result = map(lambda x, y: x + y, numbers1, numbers2)
result = list(sum_result)
print(result)
