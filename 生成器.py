from time import sleep
from tqdm import tqdm

# 因为这是生成器，tqdm不知道迭代了多少次
# 即tqdm不知道生成器何时结束，就是迭代长度不是确定的

def my_generator():
    for i in range(50):
        yield i

for _ in tqdm(my_generator()):
    sleep(0.5)




# def my_generator():
#     for i in range(50):
#         yield i
#
# for _ in tqdm(my_generator(), total = 50):
#     sleep(0.5)