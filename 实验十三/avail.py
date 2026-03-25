
# -*- coding: utf-8 -*-
"""
@author: zzk
"""

import time
import os
import cv2
import numpy as np
from numpy.linalg import inv

#进行划窗处理，固定划窗，行间隔为50，获取左上角位置
def sliding_window(img1, img2, patch_size=(100,302), istep=50):

    Ni, Nj = (int(s) for s in patch_size)
    for i in range(0, img1.shape[0] - Ni+1, istep):
        patch = (img1[i:i + Ni, 39:341], img2[i:i + Ni, 39:341])
        yield (i, 39), patch

#预测斑马线，1为斑马线，0为背景
def predict(patches, DEBUG):
    labels = np.zeros(len(patches))
    index = 0
    for Amplitude, theta in patches:
        #过滤梯度太小的点
        mask = (Amplitude>25).astype(np.float32)
        h, b = np.histogram(theta[mask.astype(bool)], bins=range(0,80,5))
        low, high = b[h.argmax()], b[h.argmax()+1]
        #统计直方图峰值方向的点数
        newmask = ((Amplitude>25) * (theta<=high) * (theta>=low)).astype(np.float32)
        value = ((Amplitude*newmask)>0).sum()

        #进行阈值设置，根据不同的场景进行调节
        if value > 1500:
            labels[index] = 1
        index += 1
        #调试模式下，打印相关的参数
        if(DEBUG):
            print(h) 
            print(low, high)
            print(value)
            cv2.imshow("newAmplitude", Amplitude*newmask)
            cv2.waitKey(0)
            
    return labels

#图片域处理，获取蓝色通道信息，进行中值滤波、开运算和闭运算
def preprocessing(img):
    kernel1 = np.ones((3,3),np.uint8)
    kernel2 = np.ones((5,5),np.uint8)
    gray = img[:,:,0]
    #中值滤波
    gray = cv2.medianBlur(gray,5)
    #开运算
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel1,iterations=4)
    #闭运算
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel2,iterations=3)
    return gray

#计算x轴和y轴的倒数，来计算梯度和方向
def getGD(canny):
    #计算x轴和y轴的sobel因子
    sobelx=cv2.Sobel(canny,cv2.CV_32F,1,0,ksize=3)
    sobely=cv2.Sobel(canny,cv2.CV_32F,0,1,ksize=3)
    #计算梯度和方向
    theta = np.arctan(np.abs(sobely/(sobelx+1e-10)))*180/np.pi
    Amplitude = np.sqrt(sobelx**2+sobely**2)
    mask = (Amplitude>30).astype(np.float32)
    Amplitude = Amplitude*mask
    return Amplitude, theta


#计算斑马线的位置，如果存在斑马线，将合并所有的划窗得到最到最终的斑马线位置
def getlocation(indices, labels, Ni, Nj):
    """
    计算斑马线的位置，如果存在斑马线，将合并所有的划窗得到最终的斑马线位置
    参数:
        indices: 所有窗口的左上角坐标数组
        labels: 每个窗口的预测结果（1表示斑马线，0表示背景）
        Ni: 窗口高度
        Nj: 窗口宽度
    返回:
        ret: 是否存在斑马线（True/False）
        location: 如果存在斑马线，返回((x_min, y_min), (x_max, y_max))，否则为None
    """
    # 获取所有被预测为斑马线的窗口的索引
    zebra_indices = indices[labels == 1]
    
    # 如果没有检测到斑马线，返回False和None
    if len(zebra_indices) == 0:
        return False, None
    
    # 提取所有斑马线窗口的左上角坐标
    # zebra_indices 是二维数组，第一列是y坐标，第二列是x坐标
    y_coords = zebra_indices[:, 0]  # 所有窗口的顶部y坐标
    x_coords = zebra_indices[:, 1]  # 所有窗口的左侧x坐标
    
    # 计算包围所有斑马线窗口的最小矩形区域
    x_min = np.min(x_coords)
    y_min = np.min(y_coords)
    x_max = np.max(x_coords) + Nj  # 加上窗口宽度
    y_max = np.max(y_coords) + Ni  # 加上窗口高度
    
    return True, ((x_min, y_min), (x_max, y_max))



##--------------------------------------------Stduent Program-------------------------------------------------------##
#############################################根据提示进行编写程序###########################################################
#   LabName：                                 人工智能小车斑马线识别实验
#   Task：   1.判断是否有斑马线，使用if.....else循环语句，同时将合并所有的划窗得到最终的斑马线位置




########################################################################################################################
##------------------------------------------Student Programl End------------------------------------------------------##



if __name__ == "__main__":
    #调试模式开关
    DEBUG = False
    #划窗的左上角
    Ni, Nj = (100, 302)

    #获取图片一定区间的位置，计算位置
    M = np.array([[-1.86073726e-01, -5.02678929e-01,  4.72322899e+02],
                 [-1.39150388e-02, -1.50260445e+00,  1.00507430e+03],
                 [-1.77785988e-05, -1.65517173e-03,  1.00000000e+00]])
 
    iM = inv(M)
    xy = np.zeros((640,640,2),dtype=np.float32)
    for py in range(640):
        for px in range(640):
            xy[py,px] = np.array([px,py],dtype=np.float32)
    ixy=cv2.perspectiveTransform(xy,iM)
    mpx,mpy = cv2.split(ixy)
    mapx,mapy=cv2.convertMaps(mpx,mpy,cv2.CV_16SC2)

    #导入视频
    cap = cv2.VideoCapture("F:\\PycharmProjects\\pythonProject\\大四上专项课\\人工智能基础算法（学生版）\\LAB13\\斑马线2.mp4")
    time.sleep(1)
    NUM_FRAMES = int(cap.get(7))
    for ii in range(NUM_FRAMES):
        print("frame: ", ii)
        ret, frame = cap.read()
        #图片重映射，将原始图片的制定位置映射为新的图片
        img = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
        # img =frame
        img = cv2.resize(img, (400,400))
        gray = preprocessing(img)
    
        canny = cv2.Canny(gray,30,90,apertureSize = 3)

        Amplitude, theta = getGD(canny)

    
        indices, patches = zip(*sliding_window(Amplitude, theta, patch_size=(Ni, Nj)))
        labels = predict(patches, DEBUG)
        indices = np.array(indices)
        ret, location = getlocation(indices, labels, Ni, Nj)
        #画图
        if ret:
           cv2.rectangle(img, location[0], location[1], (255, 0, 255), 3)
        cv2.imshow("img", img)
        cv2.waitKey(1)
      

            







