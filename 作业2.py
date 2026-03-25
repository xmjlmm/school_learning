import cv2
import numpy as np

# 打开摄像头
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(1)  # 尝试索引为 1 的摄像头
# cap = cv2.VideoCapture(2)  # 尝试索引为 2 的摄像头

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头，请检查设备连接。")
    exit()

# 读取摄像头的一帧图像
ret, frame = cap.read()

# 释放摄像头资源
cap.release()

# 检查是否成功读取图像
if not ret:
    print("无法读取图像，请检查摄像头。")
    exit()

# 将图像从 BGR 颜色空间转换到 HSV 颜色空间
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# 创建一个掩码，筛选出特定 HSV 值范围内的区域
# 设置 HSV 的范围以识别橙色
# H:5~17(橙色到黄色的范围)
# S:100~255(排除较低的饱和度，避免灰色地板干扰)
# V:50~255(亮度不要太低，以避免在非常暗的区域误识别)
mask = cv2.inRange(hsv, np.array([5, 100, 50]), np.array([17, 255, 255]))

# 根据掩码计算 HSV 图像色调(H 通道)的直方图
hist = cv2.calcHist([hsv], [0], mask, [180], [0, 180])

# 归一化直方图，使其范围为 0~255
cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)

# 设置初始跟踪窗口的位置和大小
track_window = (0, 0, frame.shape[1], frame.shape[0])

# 计算反向投影
dst = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)

# 应用 CamShift 算法进行目标跟踪
ret, track_window = cv2.CamShift(dst, track_window, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))

# 获取旋转矩形的 4 个顶点
pts = cv2.boxPoints(ret)
pts = np.int0(pts)

# 在图像上绘制轮廓
cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

# 显示处理后的图像
cv2.imshow('Tracking Result', frame)

# 按任意键关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()


