# import speech_recognition as sr
# from playsound import playsound
# import soundfile as sf  # 用于保存音频文件

# def record_audio(filename, duration=5):
#     """
#     录制音频并保存为WAV文件
#     :param filename: 保存的文件名
#     :param duration: 录制时长（秒）
#     """
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("请开始录音...（环境噪音校准中）")
#         r.adjust_for_ambient_noise(source, duration=1)  # 校准环境噪音1秒
#         print(f"正在录制 {duration} 秒音频...")
#         audio_data = r.record(source, duration=duration)
#         print("录音结束。")

#         # 保存音频
#         with open(filename, "wb") as f:
#             f.write(audio_data.get_wav_data())
#         print(f"音频已保存为: {filename}")

#         # 播放录音（可选）
#         try:
#             playsound(filename)
#         except Exception as e:
#             print(f"播放音频时出错: {e}")

# # 示例：录制一段5秒的音频，保存为 SUES.WAV
# record__audio("SUES.WAV", duration=5)




# from pydub import AudioSegment
# def convert_m4a_to_wav(m4a_file, wav_file):
#    audio = AudioSegment.from_file(m4a_file, format="m4a")
#    audio.export(wav_file, format="wav")
# convert_m4a_to_wav("F:\\学习\\大四上\\语音识别技术\\1.m4a", "converted.wav")

# import speech_recognition as sr

# def recognize_speech_from_wav(wav_file_path):
#     """
#     使用 SpeechRecognition 库识别 WAV 文件中的语音并转换为文字
#     :param wav_file_path: WAV 文件的路径
#     """
#     # 创建一个识别器实例
#     recognizer = sr.Recognizer()

#     # 使用音频文件作为源
#     with sr.AudioFile(wav_file_path) as source:
#         # 从文件中读取音频数据
#         audio_data = recognizer.record(source)
        
#     # 尝试使用识别引擎进行识别
#     try:
#         # 使用 Google Web Speech API 识别中文（需要网络连接）
#         text = recognizer.recognize_google(audio_data, language='zh-CN')
#         print(f"识别结果 (Google): {text}")
#         return text
#     except sr.UnknownValueError:
#         print("Google Web Speech API 无法理解音频内容")
#     except sr.RequestError as e:
#         print(f"无法从 Google Web Speech API 获取结果；请检查网络连接或API密钥。错误详情: {e}")
    
#     # 如果 Google 识别失败或未联网，可以尝试使用离线的 Sphinx（需安装pocketsphinx）
#     try:
#         # 使用 CMU Sphinx 引擎识别中文（离线）
#         text_sphinx = recognizer.recognize_sphinx(audio_data, language='zh-CN')
#         print(f"识别结果 (Sphinx): {text_sphinx}")
#         return text_sphinx
#     except sr.UnknownValueError:
#         print("Sphinx 无法理解音频内容")
#     except sr.RequestError as e:
#         print(f"Sphinx 引擎错误; {e}")
    
#     return None

# # 在你转换完成的 WAV 文件上调用识别函数
# recognized_text = recognize_speech_from_wav("converted.wav")

# # 你可以对 recognized_text 进行后续处理，例如写入文件等。
# if recognized_text:
#     with open("recognized_text.txt", "w", encoding='utf-8') as text_file:
#         text_file.write(recognized_text)
#     print("识别结果已写入 'recognized_text.txt'")




# from pydub import AudioSegment
# def convert_m4a_to_wav(m4a_file, wav_file):
#    audio = AudioSegment.from_file(m4a_file, format="m4a")
#    audio.export(wav_file, format="wav")
# convert_m4a_to_wav("F:\\学习\\大四上\\语音识别技术\\1.m4a", "converted.wav")

import speech_recognition as sr
from playsound import playsound
import soundfile as sf  # 用于保存音频文件

def record_audio(filename, duration=5):
    """
    录制音频并保存为WAV文件
    :param filename: 保存的文件名
    :param duration: 录制时长（秒）
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("请开始录音...（环境噪音校准中）")
        r.adjust_for_ambient_noise(source, duration=2)  # 校准环境噪音1秒
        print(f"正在录制 {duration} 秒音频...")
        audio_data = r.record(source, duration=duration)
        print("录音结束。")

        # 保存音频
        with open(filename, "wb") as f:
            f.write(audio_data.get_wav_data())
        print(f"音频已保存为: {filename}")

        # 播放录音（可选）
        try:
            playsound(filename)
        except Exception as e:
            print(f"播放音频时出错: {e}")

# 示例：录制一段4秒的音频，保存为 SUES.WAV
record_audio("F:\\学习\\大四上\\语音识别技术\\.wav", duration=4)






