# import librosa
# import matplotlib.pyplot as plt
# #1. 加载音频文件
# file_path = "F:\\学习\\大四上\\语音识别技术\\6.wav"
# y, sr = librosa.load(file_path, sr = 8000, offset = 0.08, duration = 1)
# #2. 绘制图形
# plt.figure()
# #3. 以波形图显示
# librosa.display.waveplot(y, sr)
# plt.title("Waveform")



import librosa
import librosa.display
import matplotlib.pyplot as plt

# 1. 加载音频文件
file_path = "F:\\学习\\大四上\\语音识别技术\\a_woman.wav"
# 8000采样率, y为音频数据, sr为采样率, offset为音频的开始时间, duration为音频的持续时间
y, sr = librosa.load(file_path, sr=8000, offset=0.0, duration=4)

# 2. 创建图形
plt.figure(figsize=(10, 4))

# 3. 绘制波形图（新版本Librosa使用waveshow）
librosa.display.waveshow(y, sr=sr, color="blue", alpha=0.8)

# 4. 添加标题和标签
plt.title("Audio Waveform")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.grid(True, linestyle='--', alpha=0.6)

# 5. 自动调整布局并显示图形
plt.tight_layout()
plt.show()