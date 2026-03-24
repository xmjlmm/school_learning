import numpy as np
from scipy.signal import welch
import pandas as pd

# 指定Excel文件的路径
file_path = "C:/Users/86159/Desktop/数模.xlsx.xlsx"

# 读取Excel文件的数据，并将数据存储为 DataFrame 格式
df = pd.read_excel(file_path,engine='openpyxl')

# 显示数据
print(df)



