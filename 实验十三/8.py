# -*- coding: utf-8 -*-
"""
优化版斑马线检测代码
综合多种特征提高检测精度和效率
"""

import cv2
import numpy as np
import time

def sliding_window(img1, img2, patch_size=(100, 302), istep=30, jstep=100):
    """
    改进的滑动窗口函数，支持全图像检测和多尺度
    参数:
        img1: 梯度幅值图像
        img2: 梯度方向图像
        patch_size: 滑动窗口大小 (高度, 宽度)
        istep: y方向步长
        jstep: x方向步长
    返回:
        生成器，产生窗口位置和内容
    """
    Ni, Nj = (int(s) for s in patch_size)
    
    # 只在下半部分图像检测（斑马线通常出现在图像下半部分）
    roi_y_start = int(img1.shape[0] * 0.4)
    
    for i in range(roi_y_start, img1.shape[0] - Ni + 1, istep):
        for j in range(0, img1.shape[1] - Nj + 1, jstep):
            patch = (img1[i:i + Ni, j:j + Nj], img2[i:i + Ni, j:j + Nj])
            yield (i, j), patch

def predict(patches, DEBUG=False):
    """
    预测斑马线，1为斑马线，0为背景
    综合多种特征提高准确性
    """
    labels = np.zeros(len(patches))
    index = 0
    
    for Amplitude, theta in patches:
        # 过滤梯度太小的点
        mask = (Amplitude > 25).astype(np.float32)
        
        if np.sum(mask) == 0:  # 没有足够的梯度点
            labels[index] = 0
            index += 1
            continue
            
        # 计算梯度方向直方图
        h, b = np.histogram(theta[mask.astype(bool)], bins=range(0, 80, 5))
        low, high = b[h.argmax()], b[h.argmax() + 1]
        
        # 统计直方图峰值方向的点数
        newmask = ((Amplitude > 25) * (theta <= high) * (theta >= low)).astype(np.float32)
        value = ((Amplitude * newmask) > 0).sum()
        
        # 计算等间隔特征（斑马线的重要特征）
        spacing_consistency = calculate_spacing_consistency(Amplitude, newmask)
        
        # 综合多个特征进行判断
        if value > 1500 and spacing_consistency > 0.6:
            labels[index] = 1
        
        index += 1
        
        if DEBUG:
            print(f"直方图: {h}")
            print(f"方向范围: {low}-{high}")
            print(f"特征值: {value}, 间隔一致性: {spacing_consistency}")
            cv2.imshow("Amplitude_mask", Amplitude * newmask)
            cv2.waitKey(0)
            
    return labels

def calculate_spacing_consistency(Amplitude, mask):
    """
    计算斑马线等间隔特征的一致性
    参数:
        Amplitude: 梯度幅值
        mask: 掩码图像
    返回:
        间隔一致性评分 (0-1)
    """
    # 提取mask中的边缘位置（y坐标）
    edges_y = np.where(mask > 0)[0]
    if len(edges_y) < 3:
        return 0
    
    # 计算相邻边缘间距
    diffs = np.diff(np.sort(edges_y))
    if len(diffs) == 0:
        return 0
    
    # 计算间距的一致性（变异系数的倒数）
    mean_diff = np.mean(diffs)
    std_diff = np.std(diffs)
    
    if mean_diff == 0:
        return 0
        
    consistency = mean_diff / (std_diff + 1e-10)  # 避免除零
    # 归一化到0-1范围
    return min(consistency / 10.0, 1.0)

def preprocessing(img):
    """
    图像预处理 - 优化参数
    获取蓝色通道信息，进行中值滤波、开运算和闭运算
    """
    kernel1 = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)
    
    # 使用蓝色通道减少黄色减速带干扰[4](@ref)
    gray = img[:, :, 0]
    
    # 中值滤波 - 增大核尺寸去除更大噪点
    gray = cv2.medianBlur(gray, 7)
    
    # 开运算去除小噪点
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel1, iterations=3)
    
    # 闭运算连接断线
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel2, iterations=2)
    
    return gray

def getGD(canny):
    """
    计算梯度和方向 - 使用Sobel算子
    """
    # 计算x轴和y轴的sobel因子
    sobelx = cv2.Sobel(canny, cv2.CV_32F, 1, 0, ksize=3)
    sobely = cv2.Sobel(canny, cv2.CV_32F, 0, 1, ksize=3)
    
    # 计算梯度和方向
    theta = np.arctan(np.abs(sobely / (sobelx + 1e-10))) * 180 / np.pi
    Amplitude = np.sqrt(sobelx**2 + sobely**2)
    
    # 过滤梯度太小的点
    mask = (Amplitude > 30).astype(np.float32)
    Amplitude = Amplitude * mask
    
    return Amplitude, theta

def getlocation(indices, labels, Ni, Nj):
    """
    计算斑马线的位置
    如果存在斑马线，将合并所有的划窗得到最终的斑马线位置
    """
    # 获取所有被预测为斑马线的窗口的索引
    zebra_indices = indices[labels == 1]
    
    # 如果没有检测到斑马线，返回False和None
    if len(zebra_indices) == 0:
        return False, None
    
    # 提取所有斑马线窗口的左上角坐标
    y_coords = zebra_indices[:, 0]  # 所有窗口的顶部y坐标
    x_coords = zebra_indices[:, 1]  # 所有窗口的左侧x坐标
    
    # 计算包围所有斑马线窗口的最小矩形区域
    x_min = np.min(x_coords)
    y_min = np.min(y_coords)
    x_max = np.max(x_coords) + Nj  # 加上窗口宽度
    y_max = np.max(y_coords) + Ni  # 加上窗口高度
    
    return True, ((x_min, y_min), (x_max, y_max))

def multi_scale_detection(Amplitude, theta, scales=[0.8, 1.0, 1.2]):
    """
    多尺度斑马线检测
    适应不同距离的斑马线
    """
    all_indices = []
    all_patches = []
    
    for scale in scales:
        scaled_Ni = int(100 * scale)
        scaled_Nj = int(302 * scale)
        
        # 调整步长以适应尺度变化
        istep = max(10, int(50 * scale))
        jstep = max(20, int(100 * scale))
        
        results = list(sliding_window(Amplitude, theta, 
                                     patch_size=(scaled_Ni, scaled_Nj),
                                     istep=istep, jstep=jstep))
        
        if results:
            indices, patches = zip(*results)
            all_indices.extend(indices)
            all_patches.extend(patches)
    
    return all_indices, all_patches

def main():
    # 调试模式开关
    DEBUG = False
    
    # 导入视频
    video_path = "F:\\PycharmProjects\\pythonProject\\大四上专项课\\人工智能基础算法（学生版）\\LAB13\\斑马线2.mp4"
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file")
        return
    
    # 获取视频信息
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"视频信息: {total_frames}帧, {fps:.2f}FPS")
    
    # 跳帧处理，提高效率
    frame_skip = 2  # 每3帧处理1帧
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        if frame_count % frame_skip != 0:
            continue
            
        print(f"处理帧: {frame_count}/{total_frames}")
        
        # 1. 图像预处理
        img = cv2.resize(frame, (400, 400))
        
        # 设置ROI，只处理下半部分图像提高效率
        roi_y_start = int(img.shape[0] * 0.4)
        roi_img = img[roi_y_start:, :]
        
        gray = preprocessing(roi_img)
        
        # 2. 边缘检测和特征提取
        canny = cv2.Canny(gray, 30, 90, apertureSize=3)
        Amplitude, theta = getGD(canny)
        
        # 3. 多尺度滑动窗口检测
        indices, patches = multi_scale_detection(Amplitude, theta)
        
        if not indices or not patches:
            # 显示原图
            cv2.imshow("Result", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
            
        # 4. 斑马线预测
        labels = predict(patches, DEBUG)
        
        # 5. 位置计算
        indices = np.array(indices)
        ret, location = getlocation(indices, labels, 100, 302)  # 使用最大窗口尺寸
        
        # 6. 结果显示
        if ret:
            # 调整坐标（加上ROI偏移量）
            adjusted_loc = (
                (location[0][0], location[0][1] + roi_y_start),
                (location[1][0], location[1][1] + roi_y_start)
            )
            cv2.rectangle(img, adjusted_loc[0], adjusted_loc[1], (255, 0, 255), 3)
            print(f"检测到斑马线: {adjusted_loc}")
        
        # 显示处理结果
        cv2.imshow("Result", img)
        
        # 按'q'退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()