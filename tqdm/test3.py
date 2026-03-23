from time import sleep
from tqdm import tqdm

# desc参数就是表示出现在进度条之前的文本部分
# 意义：就是当前如果有多个进度条的话，那么通过desc参数就可以知道这个进度条表示什么含义的

for _ in tqdm(range(1000), desc = 'desc参数出现在这里'):
    sleep(0.01)