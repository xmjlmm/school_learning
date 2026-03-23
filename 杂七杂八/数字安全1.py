# import cv2
# import numpy as np


# def hide_message(image_path, message, save_path):
#     """
#     在图像中隐藏信息
#     :param image_path: 原始图像路径
#     :param message: 要隐藏的信息
#     :param save_path: 保存嵌入信息后图像的路径
#     """
#     img = cv2.imread(image_path)
#     if img is None:
#         print(f"无法读取图像: {image_path}")
#         return
#     height, width, channels = img.shape
#     # 将信息转换为二进制形式，并添加结束标志
#     binary_message = ''.join(format(ord(c), 'b').zfill(8) for c in message) + '00000000'
#     index = 0
#     for h in range(height):
#         for w in range(width):
#             for c in range(channels):
#                 if index < len(binary_message):
#                     # 将信息的二进制位嵌入到像素值的最低有效位
#                     img[h, w, c] = img[h, w, c] & 0xFE | int(binary_message[index])
#                     index += 1
#                 else:
#                     break
#     # 保存嵌入信息后的图像
#     try:
#         cv2.imwrite(save_path, img)
#         print(f"信息隐藏完成，已保存为 {save_path}")
#     except Exception as e:
#         print(f"保存图像时出错: {e}")


# def extract_message(image_path):
#     """
#     从图像中提取隐藏的信息
#     :param image_path: 嵌入信息后的图像路径
#     :return: 提取出的信息
#     """
#     img = cv2.imread(image_path)
#     if img is None:
#         print(f"无法读取图像: {image_path}")
#         return ""
#     height, width, channels = img.shape
#     binary_message = ""
#     for h in range(height):
#         for w in range(width):
#             for c in range(channels):
#                 # 从像素值的最低有效位提取二进制信息
#                 binary_message += str(img[h, w, c] & 1)
#     byte_list = [binary_message[i:i + 8] for i in range(0, len(binary_message), 8)]
#     message = ""
#     for byte in byte_list:
#         decimal_value = int(byte, 2)
#         if decimal_value == 0:  # 遇到结束标志则停止提取
#             break
#         message += chr(decimal_value)
#     return message


# # 使用示例
# if __name__ == "__main__":
#     original_image_path = r"C:\Users\86159\Desktop\3.png"  
#     secret_message = "This is a secret message. Hope you can find it!"  
#     save_path = r"C:\Users\86159\Desktop\hidden_image.png"
#     hide_message(original_image_path, secret_message, save_path)
#     extracted_message = extract_message(save_path)
#     print("提取的信息为:", extracted_message)


import cv2
import numpy as np

def hide_message(image_path, message, save_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图像: {image_path}")
        return
    # 处理灰度图
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    height, width, channels = img.shape
    
    # 转换消息为二进制并填充
    binary_message = ''.join(format(ord(c), '08b') for c in message) + '00000000'
    if len(binary_message) % 8 != 0:
        binary_message += '0' * (8 - len(binary_message) % 8)
    
    index = 0
    for h in range(height):
        for w in range(width):
            for c in range(channels):
                if index >= len(binary_message):
                    break
                # 修改最低有效位
                img[h, w, c] = (img[h, w, c] & 0xFE) | int(binary_message[index])
                index += 1
    cv2.imwrite(save_path, img)
    print(f"信息已隐藏并保存至 {save_path}")

def extract_message(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法读取图像: {image_path}")
        return ""
    height, width, channels = img.shape
    
    binary_message = []
    for h in range(height):
        for w in range(width):
            for c in range(channels):
                binary_message.append(str(img[h, w, c] & 1))
    
    # 分割为8位字节并解码
    message = []
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) < 8: break
        if int(''.join(byte), 2) == 0: break
        message.append(chr(int(''.join(byte), 2)))
    return ''.join(message)

# 测试示例
if __name__ == "__main__":
    original_image = r"C:\Users\86159\Desktop\3.png"   # 确保是PNG格式且为三通道
    secret = "sues"
    hidden_image = r"C:\Users\86159\Desktop\hidden_image.png"
    
    hide_message(original_image, secret, hidden_image)
    extracted = extract_message(hidden_image)
    print(f"提取的信息: {extracted}")  # 应输出 "sues"
