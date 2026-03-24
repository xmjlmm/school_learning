import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
'''
# 指定Excel文件的路径
file_path = "C:/Users/86159/Desktop/数模.xlsx.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')
data = df
signal = np.array(data)
fft_result = np.fft.fft(signal)
'''

t = np.linspace(0, 1, 3000)

file_path = "C:/Users/86159/Desktop/data_new.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')
data = df
signal = np.array(data)
fft_result = np.fft.fft(signal)

# 计算频谱
magnitude_spectrum = np.abs(fft_result)
frequency = np.fft.fftfreq(len(t), t[1]-t[0])

# 绘制原始信号和频谱图像
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, signal)
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