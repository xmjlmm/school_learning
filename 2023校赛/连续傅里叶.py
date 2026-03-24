import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import pandas as pd
# 生成信号数据
t = np.linspace(0, 2*np.pi, 3000)  # 时间变量，从0到2π
# 指定Excel文件的路径
file_path = "C:/Users/86159/Desktop/data_new.xlsx"
# 读取Excel文件的数据，并将数据存储为 DataFrame 格式
df = pd.read_excel(file_path, engine='openpyxl')
data = df
signal = np.array(data)
# 连续傅里叶变换
freq = fftfreq(len(t), t[1]-t[0])  # 计算频率轴
transformed = fft(signal)  # 进行傅里叶变换
# 绘制原始信号和频谱图
fig, ax = plt.subplots(2, 1)
ax[0].plot(t, signal)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[0].set_title('Original Signal')
ax[1].plot(freq, np.abs(transformed))
ax[1].set_xlabel('Frequency')
ax[1].set_ylabel('Amplitude')
ax[1].set_title('Frequency Spectrum')
plt.tight_layout()
plt.show()