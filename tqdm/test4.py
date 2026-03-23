from time import sleep
from tqdm import tqdm

students = ['John', 'Jane', 'Alice', 'Bob', 'Emily', 'David', 'Mike', 'Sophia', 'James', 'Emma']

for _ in tqdm(students):
    sleep(0.5)