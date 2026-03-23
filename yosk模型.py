# from vosk import Model, KaldiRecognizer 
# import wave
# import json


# a1 = Model("D:\\vosk-model-cn-0.22")





from vosk import Model, KaldiRecognizer
import wave
import json

a1 = Model("D:\\vosk-model-cn-0.22")
# a1 = Model("D:\\vosk-model-small-cn-0.22")
a2 = wave.open("F:\\学习\\大四上\\语音识别技术\\6.wav")

a3 = KaldiRecognizer(a1, a2.getframerate())
print('开始识别')
while True:
    a4 = a2.readframes(4000)
    if not a4:
        break
    a3.AcceptWaveform(a4)
a5 = json.loads(a3.FinalResult())
print(a5)
    



# from vosk import Model, KaldiRecognizer
# import json
# from pydub import AudioSegment
# import io

# # 1. 转换 M4A 为 WAV（符合 Vosk 要求）
# m4a_audio = AudioSegment.from_file("F:\\学习\\大四上\\语音识别技术\\1.m4a", format="m4a")
# # 转换为单声道、16kHz、16位深度的PCM WAV
# wav_audio = m4a_audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
# # 将音频数据存入字节流
# wav_buffer = io.BytesIO()
# wav_audio.export(wav_buffer, format="wav")
# wav_data = wav_buffer.getvalue()

# # 2. 加载 Vosk 模型
# model_path = "D:\\vosk-model-cn-0.22"
# model = Model(model_path)

# # 3. 从字节流创建识别器
# rec = KaldiRecognizer(model, 16000)
# print('开始识别')

# # 4. 处理音频数据
# rec.AcceptWaveform(wav_data)
# result = json.loads(rec.FinalResult())
# print(result['text'])