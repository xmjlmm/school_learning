# -*- coding: utf-8 -*-
"""
@author: zzk
修改说明：移除了图像重映射处理，直接使用原始视频帧进行斑马线检测
"""

import time
import os
import cv2
import numpy as np

# 进行滑动窗口处理，固定窗口大小，行间隔为50，获取左上角位置
def sliding_window(img1, img2, patch_size=(100, 302), istep=50):
    Ni, Nj = (int(s) for s in patch_size)
    for i in range(0, img1.shape[0] - Ni + 1, istep):
        # 修改：使用整个图像宽度而不是固定区域(39:341)
        patch = (img1[i:i + Ni, :], img2[i:i + Ni, :])
        yield (i, 0), patch

# 预测斑马线，1为斑马线，0为背景
def predict(patches, DEBUG):
    labels = np.zeros(len(patches))
    index = 0
    for Amplitude, theta in patches:
        # 过滤梯度太小的点
        mask = (Amplitude > 25).astype(np.float32)
        # 修复：将 np.bool 替换为 bool
        h, b = np.histogram(theta[mask.astype(bool)], bins=range(0, 80, 5))
        low, high = b[h.argmax()], b[h.argmax() + 1]
        # 统计直方图峰值方向的点数
        newmask = ((Amplitude > 25) * (theta <= high) * (theta >= low)).astype(np.float32)
        value = ((Amplitude * newmask) > 0).sum()

        # 进行阈值设置，根据不同的场景进行调节
        if value > 1500:
            labels[index] = 1
        index += 1
        # 调试模式下，打印相关的参数
        if DEBUG:
            print(h) 
            print(low, high)
            print(value)
            cv2.imshow("newAmplitude", Amplitude * newmask)
            cv2.waitKey(0)
            
    return labels

# 图片预处理，获取蓝色通道信息，进行中值滤波、开运算和闭运算
def preprocessing(img):
    kernel1 = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)
    gray = img[:, :, 0]
    # 中值滤波
    gray = cv2.medianBlur(gray, 5)
    # 开运算
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel1, iterations=4)
    # 闭运算
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel2, iterations=3)
    return gray

# 计算x轴和y轴的导数，来计算梯度和方向
def getGD(canny):
    # 计算x轴和y轴的sobel因子
    sobelx = cv2.Sobel(canny, cv2.CV_32F, 1, 0, ksize=3)
    sobely = cv2.Sobel(canny, cv2.CV_32F, 0, 1, ksize=3)
    # 计算梯度和方向
    theta = np.arctan(np.abs(sobely / (sobelx + 1e-10))) * 180 / np.pi
    Amplitude = np.sqrt(sobelx**2 + sobely**2)
    mask = (Amplitude > 30).astype(np.float32)
    Amplitude = Amplitude * mask
    return Amplitude, theta

# 计算斑马线的位置，如果存在斑马线，将合并所有的滑动窗口得到最终的斑马线位置
def getlocation(indices, labels, Ni, Nj):
    """
    判断是否有斑马线，并计算斑马线的位置
    
    参数:
    indices: 滑动窗口的左上角坐标数组
    labels: 每个窗口的预测标签（1表示斑马线，0表示背景）
    Ni: 窗口高度
    Nj: 窗口宽度
    
    返回:
    ret: 是否有斑马线（1表示有，0表示无）
    location: 斑马线位置元组 ((xmin, ymin), (xmax, ymax)) 或 None
    """
    # 判断是否有斑马线
    zc = indices[labels == 1]
    if len(zc) == 0:
        return 0, None
    else:
        # 合并所有的滑动窗口得到最终的斑马线位置
        xmin = int(min(zc[:, 1]))
        ymin = int(min(zc[:, 0]))
        xmax = int(xmin + Nj)
        ymax = int(max(zc[:, 0]) + Ni)
        return 1, ((xmin, ymin), (xmax, ymax))

if __name__ == "__main__":
    # 调试模式开关
    DEBUG = False
    # 滑动窗口的大小
    Ni, Nj = (100, 302)

    # 导入视频
    cap = cv2.VideoCapture("F:\\PycharmProjects\\pythonProject\\大四上专项课\\人工智能基础算法（学生版）\\LAB13\\斑马线2.mp4")
    time.sleep(0.5)
    
    # 获取视频信息
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    NUM_FRAMES = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"视频信息: {width}x{height}, {fps}FPS, 总帧数: {NUM_FRAMES}")
    
    for ii in range(NUM_FRAMES):
        print("frame: ", ii)
        ret, frame = cap.read()
        if not ret:
            break
            
        # 修改：直接使用原始帧，不进行重映射
        img = frame.copy()
        
        # 可选：调整图像大小（如果需要）
        # img = cv2.resize(img, (800, 400))
        
        gray = preprocessing(img)
    
        canny = cv2.Canny(gray, 30, 90, apertureSize=3)
        Amplitude, theta = getGD(canny)

        # 生成滑动窗口并预测
        indices_patches = list(sliding_window(Amplitude, theta, patch_size=(Ni, Nj)))
        if indices_patches:
            indices, patches = zip(*indices_patches)
            labels = predict(patches, DEBUG)
            indices = np.array(indices)
            ret, location = getlocation(indices, labels, Ni, Nj)
            
            # 画图
            if ret:
                cv2.rectangle(img, location[0], location[1], (255, 0, 255), 3)
                print(f"检测到斑马线: {location}")
            
            cv2.imshow("Original Frame", img)
            cv2.imshow("Processed", gray)
            cv2.imshow("Canny", canny)
            
            # 退出条件
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # 释放资源
    cap.release()
    cv2.destroyAllWindows()