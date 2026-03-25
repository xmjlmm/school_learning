import cv2
import numpy as np
import time

def sliding_window(img1, img2, patch_size=(100, 302), istep=30, jstep=100):
    """
    滑动窗口函数，在全图像范围内检测斑马线
    """
    Ni, Nj = (int(s) for s in patch_size)
    
    # 只在下半部分图像检测（斑马线通常出现在图像下半部分）
    roi_y_start = int(img1.shape[0] * 0.4)
    
    for i in range(roi_y_start, img1.shape[0] - Ni + 1, istep):
        for j in range(0, img1.shape[1] - Nj + 1, jstep):
            patch = (img1[i:i + Ni, j:j + Nj], img2[i:i + Ni, j:j + Nj])
            yield (i, j), patch

def calculate_spacing_consistency(Amplitude, mask):
    """
    计算斑马线等间隔特征的一致性
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
        
    consistency = mean_diff / (std_diff + 1e-10)
    return min(consistency / 10.0, 1.0)

def predict(patches, DEBUG=False):
    """
    预测斑马线，1为斑马线，0为背景
    """
    labels = np.zeros(len(patches))
    index = 0
    
    for Amplitude, theta in patches:
        # 过滤梯度太小的点
        mask = (Amplitude > 25).astype(np.float32)
        
        if np.sum(mask) == 0:
            labels[index] = 0
            index += 1
            continue
            
        # 计算梯度方向直方图
        h, b = np.histogram(theta[mask.astype(bool)], bins=range(0, 80, 5))
        low, high = b[h.argmax()], b[h.argmax() + 1]
        
        # 统计直方图峰值方向的点数
        newmask = ((Amplitude > 25) * (theta <= high) * (theta >= low)).astype(np.float32)
        value = ((Amplitude * newmask) > 0).sum()
        
        # 计算等间隔特征
        spacing_consistency = calculate_spacing_consistency(Amplitude, newmask)
        
        # 综合多个特征进行判断
        if value > 1300 and spacing_consistency > 0.02:  # 降低阈值以提高检测率
            labels[index] = 1
        
        index += 1
        
        if DEBUG:
            print(f"窗口{index}: 特征值={value}, 间隔一致性={spacing_consistency}")
            
    return labels

def preprocessing(img):
    """
    图像预处理
    """
    kernel1 = np.ones((3, 3), np.uint8)
    kernel2 = np.ones((5, 5), np.uint8)
    
    # 使用蓝色通道减少黄色减速带干扰[1](@ref)
    gray = img[:, :, 0]
    
    # 中值滤波
    gray = cv2.medianBlur(gray, 5)
    
    # 形态学操作
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel1, iterations=3)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel2, iterations=2)
    
    return gray

def getGD(canny):
    """
    计算梯度和方向
    """
    sobelx = cv2.Sobel(canny, cv2.CV_32F, 1, 0, ksize=3)
    sobely = cv2.Sobel(canny, cv2.CV_32F, 0, 1, ksize=3)
    
    theta = np.arctan(np.abs(sobely / (sobelx + 1e-10))) * 180 / np.pi
    Amplitude = np.sqrt(sobelx**2 + sobely**2)
    
    mask = (Amplitude > 30).astype(np.float32)
    Amplitude = Amplitude * mask
    
    return Amplitude, theta

def getlocation(indices, labels, Ni, Nj):
    """
    计算斑马线的位置
    """
    zebra_indices = indices[labels == 1]
    
    if len(zebra_indices) == 0:
        return False, None
    
    y_coords = zebra_indices[:, 0]
    x_coords = zebra_indices[:, 1]
    
    x_min = np.min(x_coords)
    y_min = np.min(y_coords)
    x_max = np.max(x_coords) + Nj
    y_max = np.max(y_coords) + Ni
    
    return True, ((x_min, y_min), (x_max, y_max))

def main():
    DEBUG = True  # 启用调试模式
    
    # 请确保视频路径正确
    video_path = "F:\\PycharmProjects\\pythonProject\\大四上专项课\\人工智能基础算法（学生版）\\LAB13\\斑马线2.mp4"
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("错误：无法打开视频文件，请检查路径")
        return
    
    print("✅ 视频文件打开成功")
    
    # 获取视频信息
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"视频信息: {total_frames}帧, {fps:.2f}FPS")
    
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("视频读取结束")
            break
            
        frame_count += 1
        if frame_count % 2 != 0:  # 处理每2帧
            continue
            
        print(f"\n处理帧: {frame_count}/{total_frames}")
        
        # 1. 图像预处理
        img = cv2.resize(frame, (400, 400))
        
        # 设置ROI，只处理下半部分图像
        roi_y_start = int(img.shape[0] * 0.4)
        roi_img = img[roi_y_start:, :]
        
        gray = preprocessing(roi_img)
        
        if DEBUG:
            cv2.imshow("1. Preprocessed", gray)
            cv2.waitKey(1)
        
        # 2. 边缘检测和特征提取
        canny = cv2.Canny(gray, 30, 90, apertureSize=3)
        Amplitude, theta = getGD(canny)
        
        if DEBUG:
            amp_vis = cv2.normalize(Amplitude, None, 0, 255, cv2.NORM_MINMAX)
            cv2.imshow("2. Gradient Amplitude", amp_vis.astype(np.uint8))
            cv2.waitKey(1)
        
        # 3. 滑动窗口检测
        patches_list = list(sliding_window(Amplitude, theta))
        
        if not patches_list:
            print("未找到任何窗口")
            cv2.imshow("Result", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        
        indices, patches = zip(*patches_list)
        print(f"找到 {len(patches)} 个窗口")
        
        # 4. 斑马线预测
        labels = predict(patches, DEBUG)
        zebra_count = np.sum(labels == 1)
        print(f"检测到 {zebra_count} 个斑马线窗口")
        
        # 5. 位置计算
        indices = np.array(indices)
        ret, location = getlocation(indices, labels, 100, 302)
        
        # 6. 结果显示
        if ret:
            adjusted_loc = (
                (location[0][0], location[0][1] + roi_y_start),
                (location[1][0], location[1][1] + roi_y_start)
            )
            cv2.rectangle(img, adjusted_loc[0], adjusted_loc[1], (255, 0, 255), 3)
            print(f"检测到斑马线: {adjusted_loc}")
        else:
            print("未检测到斑马线")
        
        # 显示处理结果
        cv2.imshow("Result", img)
        
        # 按'q'退出
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()