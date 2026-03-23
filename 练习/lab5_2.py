def isNarcissus(n):
    a = n // 100
    b = (n // 10) % 10
    c = n % 10
    if n == a ** 3 + b ** 3 + c ** 3:
        return True

    return False


for n in range(100, 1000):
    if isNarcissus(n) == True:
        print(n)