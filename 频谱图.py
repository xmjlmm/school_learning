import numpy as np
import matplotlib
import librosa
import matplotlib.pyplot as plt
from scipy.fftpack import fft
matplotlib.rc("font", family = "SimHei") #显示中文
matplotlib.rcParams["axes.unicode_minus"] = False #显示负号
#1. 加载一个音频文件
file_path = "F:\\学习\\大四上\\语音识别技术\\a_woman.wav"
x,sr = librosa.load(file_path, sr = 8000, offset = 0.08, duration = 4)
#2. 对时频信号做快速傅立叶变换
ft = fft(x)
#2.1 获取幅度和频率
magnitude = np.absolute(ft) #对fft的结果直接取模，得到幅度
frequency = np.linspace(0, sr, len(magnitude)) #具体值为（0，16000，121632）
#3. 绘制图形，横坐标是frequency，纵坐标是magnitude
plt.plot(frequency, magnitude)
plt.title("频谱图(Spectrum)")
plt.xlabel("Frequency(Hz)")
plt.ylabel("Amplitude(dB)")
plt.show()
