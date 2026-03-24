import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pandas as pd

# 输入信号
t = np.linspace(0, 1, 9212)  # 创建一个从0到1的等间距时间数组作为输入信号的时间轴

# 指定Excel文件的路径
file_path = "C:/Users/86159/Desktop/数模.xlsx.xlsx"

# 读取Excel文件的数据，并将数据存储为 DataFrame 格式
df = pd.read_excel(file_path, engine='openpyxl')

# 显示数据
print(df)
# 示例信号序列
data = df
x = np.array(data)
# 假设信号数据为signal，长度为N


# 短时傅里叶变换
f, t_spec, spec = signal.stft(x, nperseg=100, noverlap=50)



# 切片数据数组
C = np.abs(spec)[:, :-1, :-1]

# 绘制短时傅里叶变换图
plt.pcolormesh(t_spec, f, C)

# 绘制短时傅里叶变换图

plt.colorbar(label='Magnitude')  # 添加颜色条
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.title('Short-Time Fourier Transform')
plt.show()