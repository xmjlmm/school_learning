from tqdm import tqdm
from time import sleep

# 上下文管理器
with tqdm(total = 100) as pbar:
    pbar.update(10)
    sleep(2)
    pbar.update(20)
    sleep(2)
    pbar.update(70)
