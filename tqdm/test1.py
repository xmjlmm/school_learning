from time import sleep
# 就是一个显示进度条的第三方库
from tqdm import tqdm

for _ in tqdm(range(10000)):
    sleep(0.001)