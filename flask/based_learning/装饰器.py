'''
@my_decorator 就是装饰器
装饰器的作用就是装饰被装饰的函数，在被装饰的函数执行前和执行后添加一些额外的功能

'''

def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

def main():
    say_hello()

if __name__ == "__main__":
    main()