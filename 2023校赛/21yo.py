import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import pandas as pd

# 指定Excel文件的路径
file_path = "C:/Users/86159/Desktop/数模.xlsx.xlsx"

# 读取Excel文件的数据，并将数据存储为 DataFrame 格式
df = pd.read_excel(file_path, engine='openpyxl')
data = df
new_signal = np.array(data)

# 进行傅里叶变换
fft_result = np.fft.fft(new_signal)
x = np.array([1])
y=np.array(data)
x = np.reshape(x, (y.shape[0],))
x = np.repeat(x, y.shape[0])
# 计算频谱
magnitude_spectrum = np.abs(fft_result)
frequency = np.fft.fftfreq(9212)

x_broadcasted = np.broadcast_to(x, y.shape)

# 绘制原始信号和频谱图像
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(9212, new_signal)
plt.title('Original Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')

plt.subplot(2, 1, 2)
plt.plot(frequency, magnitude_spectrum)
plt.title('Frequency Spectrum')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')

plt.tight_layout()
plt.show()