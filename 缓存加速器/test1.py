'''实际上，有一个原生的Python装饰器可以显著提高性能。我们不需要安装任何东西，因为它是Python内置的。'''


from functools import cache

def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


@cache
def fibonacci_cached(n):
    if n < 2:
        return n
    return fibonacci_cached(n-1) + fibonacci_cached(n-2)

def main():
    print(fibonacci(35))
    print(fibonacci_cached(35))
    print(fibonacci_cached.cache_info())
    print(fibonacci_cached.cache_clear())


if __name__ == '__main__':
    main()














