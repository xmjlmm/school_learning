# -*- coding: utf-8 -*-
"""
@author: zzk
改进版斑马线检测：结合边缘检测、形态学操作和轮廓分析
"""

import time
import os
import cv2
import numpy as np

def detect_zebra_crossing_improved(img, debug=False):
    """
    改进的斑马线检测函数
    返回: (has_zebra, bounding_box, processed_img)
    """
    # 1. 图像预处理 - 使用多种方法提高鲁棒性[1,7](@ref)
    # 转换为HSV颜色空间，更好地处理光照变化
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 使用HSV中的V通道(亮度)而不是蓝色通道
    gray = hsv[:, :, 2].copy()
    
    # 中值滤波去噪
    gray = cv2.medianBlur(gray, 5)
    
    # 2. 自适应阈值处理 - 替代固定阈值[1](@ref)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY, 11, 2)
    
    # 3. 形态学操作 - 增强斑马线特征[7](@ref)
    # 先开运算去除小噪声，再闭运算连接斑马线片段
    kernel1 = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)
    
    morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel1, iterations=2)
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, kernel2, iterations=3)
    
    # 4. 边缘检测 - 使用Canny算法[6,8](@ref)
    edges = cv2.Canny(morph, 50, 150, apertureSize=3)
    
    # 5. 霍夫变换检测直线 - 识别斑马线的平行线特征[8](@ref)
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=50,
                           minLineLength=100, maxLineGap=50)
    
    # 6. 分析直线特征，识别斑马线
    zebra_detected = False
    bounding_box = None
    
    if lines is not None and len(lines) > 5:  # 斑马线应有多个平行线
        # 筛选近似水平的直线（考虑视角变化）
        horizontal_lines = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            if abs(angle) < 30 or abs(angle) > 150:  # 近似水平线
                horizontal_lines.append(line[0])
        
        # 检查是否有多条平行线（斑马线特征）
        if len(horizontal_lines) >= 4:  # 至少4条线才可能是斑马线
            # 计算这些线的平均间距（斑马线应具有规律间距）
            lines_sorted = sorted(horizontal_lines, key=lambda x: x[1])
            spacings = []
            for i in range(1, len(lines_sorted)):
                spacing = abs(lines_sorted[i][1] - lines_sorted[i-1][1])
                spacings.append(spacing)
            
            # 检查间距的均匀性（斑马线间距应相对均匀）
            if len(spacings) > 2:
                avg_spacing = np.mean(spacings)
                std_spacing = np.std(spacings)
                
                # 间距相对均匀，可能是斑马线
                if std_spacing < avg_spacing * 0.5:  # 标准差小于平均间距的一半
                    zebra_detected = True
                    
                    # 计算边界框
                    y_coords = [line[1] for line in lines_sorted] + [line[3] for line in lines_sorted]
                    x_coords = [line[0] for line in lines_sorted] + [line[2] for line in lines_sorted]
                    
                    y_min, y_max = min(y_coords), max(y_coords)
                    x_min, x_max = min(x_coords), max(x_coords)
                    
                    # 扩展边界框以包含所有线条
                    padding = int(avg_spacing * 0.5)
                    bounding_box = ((max(0, x_min - padding), max(0, y_min - padding)),
                                   (min(img.shape[1], x_max + padding), min(img.shape[0], y_max + padding)))
    
    # 调试信息
    if debug:
        debug_img = img.copy()
        if zebra_detected and bounding_box:
            cv2.rectangle(debug_img, bounding_box[0], bounding_box[1], (0, 255, 0), 3)
            cv2.putText(debug_img, "Zebra Crossing", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 显示处理过程中的各阶段图像
        processing_stack = create_processing_stack(img, gray, thresh, morph, edges, debug_img)
        cv2.imshow("Processing Steps", processing_stack)
    
    return zebra_detected, bounding_box

def create_processing_stack(original, gray, thresh, morph, edges, result):
    """创建处理步骤的可视化堆栈"""
    # 调整大小以便堆叠
    height, width = original.shape[:2]
    display_size = (width // 3, height // 3)
    
    # 调整图像大小
    orig_resized = cv2.resize(original, display_size)
    gray_resized = cv2.resize(gray, display_size)
    thresh_resized = cv2.resize(thresh, display_size)
    morph_resized = cv2.resize(morph, display_size)
    edges_resized = cv2.resize(edges, display_size)
    result_resized = cv2.resize(result, display_size)
    
    # 转换为彩色以便显示（单通道图像转换为彩色）
    gray_colored = cv2.cvtColor(gray_resized, cv2.COLOR_GRAY2BGR)
    thresh_colored = cv2.cvtColor(thresh_resized, cv2.COLOR_GRAY2BGR)
    morph_colored = cv2.cvtColor(morph_resized, cv2.COLOR_GRAY2BGR)
    edges_colored = cv2.cvtColor(edges_resized, cv2.COLOR_GRAY2BGR)
    
    # 添加标签
    cv2.putText(orig_resized, 'Original', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(gray_colored, 'Gray', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(thresh_colored, 'Threshold', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(morph_colored, 'Morphology', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(edges_colored, 'Edges', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(result_resized, 'Result', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    # 堆叠图像
    top_row = np.hstack([orig_resized, gray_colored, thresh_colored])
    middle_row = np.hstack([morph_colored, edges_colored, result_resized])
    processing_stack = np.vstack([top_row, middle_row])
    
    return processing_stack

if __name__ == "__main__":
    # 初始化视频捕获
    cap = cv2.VideoCapture("F:\\PycharmProjects\\pythonProject\\大四上专项课\\人工智能基础算法（学生版）\\LAB13\\斑马线2.mp4")
    
    if not cap.isOpened():
        print("错误：无法打开视频文件")
        exit()
    
    # 获取视频信息
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"视频信息: {width}x{height}, {fps}FPS, 总帧数: {total_frames}")
    
    frame_count = 0
    detection_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        
        # 每5帧处理一次（提高处理速度）
        if frame_count % 5 != 0:
            continue
        
        # 检测斑马线
        detected, bbox = detect_zebra_crossing_improved(frame, debug=True)
        
        # 显示结果
        result_frame = frame.copy()
        if detected:
            detection_count += 1
            cv2.rectangle(result_frame, bbox[0], bbox[1], (0, 255, 0), 3)
            cv2.putText(result_frame, "Zebra Crossing Detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print(f"帧 {frame_count}: 检测到斑马线, 位置: {bbox}")
        
        cv2.imshow("Zebra Crossing Detection", result_frame)
        
        # 退出条件
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 输出统计信息
    print(f"\n检测统计:")
    print(f"总帧数: {frame_count}")
    print(f"检测到斑马线的帧数: {detection_count}")
    print(f"检测率: {detection_count/max(1, frame_count)*100:.2f}%")
    
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()