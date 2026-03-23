from tqdm import tqdm
from time import sleep

pbar = tqdm(total = 100)
pbar.update(10)
sleep(2)
pbar.update(20)
sleep(2)
pbar.update(70)
pbar.close()