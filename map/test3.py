def add_three_numbers(x, y, z):
    return x + y + z

numbers1 = [1, 2, 3]
numbers2 = [10, 20, 30]
numbers3 = [100, 200, 300]

result = list(map(add_three_numbers, numbers1, numbers2, numbers3))
print(result)
