'''在具有“副作用”的函数中不应使用缓存
所谓“副作用”，我指的是除了返回值之外的操作，例如将文本写入文件或更新数据库表。
如果我们对这些函数使用缓存，那么“副作用”将不会在第二次发生。
换句话说，它只会在我们第一次调用函数时起作用。

假设我们有一个函数，其任务是将消息追加到日志文件中，并返回该消息的长度。
如果我们对这样一个具有副作用的函数使用缓存，那么在首次执行写入操作后，
后续相同输入的调用将直接从缓存中获取结果，而不会再次执行写入操作。'''



from functools import cache
import os
# 定义一个简单的日志函数，每次调用时都会向文件写入一条消息
@cache
def log_message(message):
    # 我没有这个文件也可以吗，蛙趣，有意思
    with open("log.txt", "a") as file:
        file.write(message + "\n")
    return len(message)

# 第一次调用函数，写入消息
log_message("Hello!")

# 尝试再次调用相同的消息
log_message("Hello!")

# 查看文件内容
with open("log.txt", "r") as file:
    contents = file.readlines()

print(contents)
# 只输出一行：Hello!