import librosa
import matplotlib.pyplot as plt
import numpy as np
import librosa.display

audio_file = "F:\\学习\\大四上\\语音识别技术\\a_woman.wav"
# 通过librosa读取音频文件中的语音信号
signal, sr = librosa.load(audio_file)

# 计算MFCC，delta_MFCC，和delta_delta_MFCC
# 使用11个MFCC系数（不包括第0个能量系数），与图片中的11个维度对应
mfccs = librosa.feature.mfcc(y=signal, n_mfcc=12, sr=sr)  # 提取12个，然后去掉第0个
mfccs = mfccs[1:]  # 去掉第0个能量相关的系数，保留1-11共11个系数

delta_mfccs = librosa.feature.delta(mfccs)
delta2_mfccs = librosa.feature.delta(mfccs, order=2)

plt.figure(figsize=(15, 10))

# 设置y轴刻度，显示1,3,5,7,9,11
yticks = [1, 3, 5, 7, 9, 11]
yticks_labels = ['1', '3', '5', '7', '9', '11']

# 第一个子图：MFCC 静态特征
plt.subplot(3, 1, 1)
# 使用热力图颜色映射，与图片风格一致
img1 = librosa.display.specshow(mfccs, 
                         x_axis="time", 
                         y_axis="frames",
                         sr=sr,
                         cmap='inferno')  
plt.yticks(ticks=yticks, labels=yticks_labels)
plt.title("MFCC", fontsize=12, fontweight='bold')
plt.colorbar(img1, format="%+2.0f")
plt.ylabel("MFCC Coefficients")

# 第二个子图：delta_MFCC  一阶差分
plt.subplot(3, 1, 2)
img2 = librosa.display.specshow(delta_mfccs, 
                         x_axis="time",
                         y_axis="frames",
                         sr=sr,
                         cmap='inferno')
plt.yticks(ticks=yticks, labels=yticks_labels)
plt.title("delta MFCC", fontsize=12, fontweight='bold')
plt.colorbar(img2, format="%+2.0f")
plt.ylabel("Delta Coefficients")

# 第三个子图：delta_delta_MFCC  二阶差分
plt.subplot(3, 1, 3)
img3 = librosa.display.specshow(delta2_mfccs, 
                         x_axis="time",
                         y_axis="frames",
                         sr=sr,
                         cmap='inferno')
plt.yticks(ticks=yticks, labels=yticks_labels)
plt.title("delta delta MFCC", fontsize=12, fontweight='bold')
plt.colorbar(img3, format="%+2.0f")
plt.ylabel("Delta-Delta Coefficients")
plt.xlabel("Time (s)")

plt.tight_layout()
plt.show()