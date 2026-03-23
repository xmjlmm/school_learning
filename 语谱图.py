import librosa
from librosa import display
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

#1. 加载一个音频文件
file_path = "F:\\学习\\大四上\\语音识别技术\\a_woman.wav"
y, sr = librosa.load(file_path, sr=8000, offset=0.08, duration=4)

# 中文显示
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 准备绘图 - 修正子图创建方式
fig, ax = plt.subplots(2, 1, figsize=(10, 8))

#2. 获取时频谱矩阵
M = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

# cmap: viridis, plasma, inferno, magma, cividis, hot, coolwarm
#3.1 绘制基于线性的语谱图 - 修正函数名和参数
img1 = librosa.display.specshow(M, sr=sr, x_axis='time', y_axis='linear', ax=ax[0], cmap='magma')
ax[0].set_title('Linear-frequency power spectrogram')
plt.colorbar(img1, ax=ax[0], format='%+2.0f dB')
ax[0].label_outer()

#3.2 绘制基于log域的语谱图 - 重新计算STFT并使用正确的参数
# 使用不同的hop_length重新计算STFT
S = librosa.stft(y, hop_length=1024)
M_log = librosa.amplitude_to_db(np.abs(S), ref=np.max)

# 绘制对数频谱图
img2 = librosa.display.specshow(M_log, sr=sr, hop_length=1024, x_axis='time', y_axis='log', ax=ax[1], cmap='inferno')
plt.colorbar(img2, ax=ax[1], format='%+2.0f dB')
ax[1].set_title('语音信号的语谱图（频率为对数级）')
ax[1].set_xlabel('Time(s)')
ax[1].set_ylabel('Frequency(Hz)')
ax[1].label_outer()

plt.tight_layout()
plt.savefig("./语音信号的语谱图-对数级-hoplength-1024.png", dpi=600, bbox_inches='tight')
plt.show()