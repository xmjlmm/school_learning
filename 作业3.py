import cv2
import numpy as np

# 打开视频文件
cap = cv2.VideoCapture('F://EV录制//kafka2.0.mp4')

# 读取视频的第一帧
ret, frame = cap.read()

# 将图像从 BGR 颜色空间转换到 HSV 颜色空间
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# 创建红色范围的掩码（覆盖0°和180°附近的红色）
lower_red1 = np.array([0, 100, 50])     # 低H值红色范围
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 100, 50])   # 高H值红色范围
upper_red2 = np.array([180, 255, 255])

# 合并两个红色区域的掩码
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)

# 计算HSV图像色调通道的直方图
hist = cv2.calcHist([hsv], [0], mask, [180], [0, 180])
cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

# 设置初始跟踪窗口
track_window = (0, 0, frame.shape[1], frame.shape[0])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
    
    # 应用CamShift算法
    ret, track_window = cv2.CamShift(dst, track_window, 
                                     (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))
    
    # 绘制跟踪框
    pts = cv2.boxPoints(ret)
    pts = np.int0(pts)
    cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
    
    cv2.imshow('Tracking', frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()