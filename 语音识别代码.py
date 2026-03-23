# # import speech_recognition as sr

# # def recognize_speech_from_file(audio_file_path, language='zh-CN'):
# #     """
# #     从音频文件中识别语音内容
# #     :param audio_file_path: 音频文件路径（支持WAV格式）
# #     :param language: 识别语言（默认中文）
# #     :return: 识别出的文本（失败时返回None）
# #     """
# #     # 创建识别器对象
# #     recognizer = sr.Recognizer()
    
# #     try:
# #         # 加载音频文件
# #         with sr.AudioFile(audio_file_path) as source:
# #             audio_data = recognizer.record(source)  # 读取整个音频文件
        
# #         # 使用Google Web Speech API进行识别（需联网）
# #         text = recognizer.recognize_google(audio_data, language=language)
# #         print(f"识别结果: {text}")
# #         return text
        
# #     except sr.UnknownValueError:
# #         print("错误: 无法理解音频内容")
# #     except sr.RequestError as e:
# #         print(f"错误: 服务请求失败；{e}")
# #     except FileNotFoundError:
# #         print("错误: 音频文件不存在")
# #     except Exception as e:
# #         print(f"意外错误: {e}")
    
# #     return None

# # # 示例用法
# # if __name__ == "__main__":
# #     result = recognize_speech_from_file("F:\\学习\\大四上\\语音识别技术\\2.m4a", language="zh-CN")


# from pydub import AudioSegment
# def convert_m4a_to_wav(m4a_file, wav_file):
#    audio = AudioSegment.from_file(m4a_file, format="m4a")
#    audio.export(wav_file, format="wav")
# convert_m4a_to_wav("F:\\学习\\大四上\\语音识别技术\\1.m4a", "converted.wav")






# from pydub import AudioSegment
# import speech_recognition as sr
# import os

# def convert_m4a_to_wav(m4a_file, wav_file):
#     """
#     将M4A音频文件转换为WAV格式
#     :param m4a_file: 输入的M4A文件路径
#     :param wav_file: 输出的WAV文件路径
#     """
#     try:
#         audio = AudioSegment.from_file(m4a_file, format="m4a")
#         # 转换为单声道、16kHz采样率（提高识别准确率）
#         audio = audio.set_channels(1).set_frame_rate(16000)
#         audio.export(wav_file, format="wav")
#         print(f"转换完成: {wav_file}")
#         return True
#     except Exception as e:
#         print(f"转换过程中出错: {e}")
#         return False

# def recognize_speech_offline(audio_file_path, language='zh-CN'):
#     """
#     使用CMU Sphinx进行离线语音识别
#     :param audio_file_path: 音频文件路径（WAV格式）
#     :param language: 识别语言（默认中文）
#     :return: 识别出的文本
#     """
#     recognizer = sr.Recognizer()
    
#     try:
#         with sr.AudioFile(audio_file_path) as source:
#             # 调整环境噪声（提高识别准确率）
#             recognizer.adjust_for_ambient_noise(source)
#             audio_data = recognizer.record(source)
        
#         # 使用CMU Sphinx进行离线识别
#         text = recognizer.recognize_sphinx(audio_data, language=language)
#         print(f"识别结果: {text}")
#         return text
        
#     except sr.UnknownValueError:
#         print("Sphinx无法理解音频内容")
#     except sr.RequestError as e:
#         print(f"Sphinx引擎错误: {e}")
#     except Exception as e:
#         print(f"处理过程中出错: {e}")
    
#     return None

# # 主程序
# if __name__ == "__main__":
#     # 1. 转换M4A到WAV
#     input_file = "F:\\学习\\大四上\\语音识别技术\\2.wav"
#     output_file = "converted.wav"
    
#     if convert_m4a_to_wav(input_file, output_file):
#         # 2. 进行离线语音识别
#         recognize_speech_offline(output_file, language='zh-CN')










import speech_recognition as sr 
# Initialize the recognizer 
r = sr.Recognizer() 
# Load the audio file 
audio_file = "F:\\学习\\大四上\\语音识别技术\\6.wav"
# Use the audio file as the source 
with sr.AudioFile(audio_file) as source: 
    # Adjust for ambient noise and record the audio 
    r.adjust_for_ambient_noise(source) 
    audio_data = r.record(source) # Read the entire audio file 
# Perform speech recognition 
    try: 
        # Recognize speech using CMU Sphinx API 
        # text = r.recognize_sphinx(audio_data, language='zh-CN', show_all = True) 
        text = r.recognize_sphinx(audio_data, language='zh-CN') # 移除了 show_all = True
        print("Transcription: ", text) 
    except sr.UnknownValueError: 
        print("Sphinx API could not understand the audio") 
    except sr.RequestError as e: 
        print(f"Could not request results from Sphinx API; {e}") 







# import os
# import speech_recognition as sr
# folder_path=os.path.join(os.path.dirname(sr.__file__),'pocketsphinx-data')
# os.startfile(folder_path)





# import speech_recognition as sr
# import os

# # Initialize the recognizer
# r = sr.Recognizer()

# # Load the audio file
# audio_file = "F:\\学习\\大四上\\语音识别技术\\2.wav"

# # 设置 Vosk 模型路径 (请根据您实际解压的路径修改)
# model_path = "F:\\学习\\大四上\\语音识别技术\\vosk-model-cn-0.22"
# if not os.path.exists(model_path):
#     print(f"Vosk model path '{model_path}' does not exist. Please check the path.")
#     exit(1)

# # Use the audio file as the source
# with sr.AudioFile(audio_file) as source:
#     # Adjust for ambient noise and record the audio
#     r.adjust_for_ambient_noise(source)
#     audio_data = r.record(source)  # Read the entire audio file

# # Perform speech recognition using Vosk
# try:
#     # Recognize speech using Vosk API
#     # 注意：recognize_vosk 默认会使用系统环境变量 VOSK_MODEL_PATH 指定的模型，
#     # 如果未设置，则需要通过 language 参数指定模型路径，但 speech_recognition 库的此函数可能并不直接支持绝对路径。
#     # 更可靠的做法是设置环境变量，或者在代码中指定 Vosk 的模型路径（这需要更底层的 Vosk API 调用）。
    
#     # 以下使用 recognize_vosk，并指定语言为中文（如果模型路径已正确设置，此参数可能用于选择模型目录中的特定语言）
#     text = r.recognize_vosk(audio_data, language="cn")  # 或者 "zh-CN"，具体取决于模型支持
#     print("Vosk Transcription: ", text)
    
#     # Vosk 返回的是一个 JSON 字符串，通常包含 "text" 字段。例如：'{"text": "上海工程技术大学"}'
#     # 如果需要提取纯文本，可以解析 JSON：
#     import json
#     text_dict = json.loads(text)
#     pure_text = text_dict.get("text", "")
#     print("提取的文本: ", pure_text)

# except sr.UnknownValueError:
#     print("Vosk API could not understand the audio")
# except sr.RequestError as e:
#     print(f"Could not request results from Vosk API; {e}")


# from vosk import Model, KaldiRecognizer
# import wave
# import json

# a1 = Model("F:\\学习\\大四上\\语音识别技术\\vosk-model-cn-0.22")