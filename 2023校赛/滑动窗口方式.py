import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 指定Excel文件的路径
file_path = "C:/Users/86159/Desktop/data_new(1).xlsx"
# 读取Excel文件的数据，并将数据存储为 DataFrame 格式
df = pd.read_excel(file_path, engine='openpyxl')
# 显示数据
#print(df)
# 示例信号序列
data = df.values.flatten()  # 获取数据并展平为一维数组
signal = np.array(data)
# 假设信号数据为signal，长度为N
window_length = 100  # 子信号的长度
step_size = 1  # 步长
# 计算子信号的数量
num_windows = int((len(signal) - window_length) / step_size) + 1
# 提取子信号
sub_signals = []
for i in range(num_windows):
    start = i * step_size
    end = start + window_length
    sub_signal = signal[start:end]
    sub_signals.append(sub_signal)

# 将数据转换为DataFrame对象
df = pd.DataFrame(sub_signals, columns=[f"Sub Signal {i+1}" for i in range(window_length)])
#df = pd.DataFrame(sub_signals)
# 导出数据到Excel文件
df.to_excel("C:/Users/86159/Desktop/data_id3(1).xlsx", index=False)