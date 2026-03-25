def square(x):
    return x ** 2

numbers1 = [1, 2, 3, 4, 5]
numbers2 = [10, 20, 30]

result = list(map(square, numbers1, numbers2))
print(result)
