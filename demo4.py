for item in range(100,1000):
    a = item // 100
    b = (item - 100 * a) // 10
    c = (item - 100 * a - 10 * b)
    if item == a * a * a + b * b * b + c * c * c:
        print(item)

