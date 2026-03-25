
import cv2
import numpy as np
#打开视频文件
# cap= cv2.VideoCapture('F://EV录制//火焰特效.mp4' )
cap= cv2.VideoCapture("C://Users//86159//Desktop//test.mp4")
#读取视频的第一帧
ret, frame = cap.read( )
#将图像从 BGR颜色空间转换到 HSV 颜色空间
hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#创建一个掩码,筛选出特定HSV值范围内的区域
#设置 HSV的范围以识别橙色
#H:5~17(橙色到黄色的范围)
#S:100~255(排除较低的饱和度,避免灰色地板干扰)
#V:50~255(亮度不要太低,以避免在非常暗的区域误识别)
# print(hsv)
mask=cv2.inRange(hsv,np.array([5,100,50]),np.array([17,255,255]))#根据掩码计算HSV图像色调(日通道)的直方图
hist=cv2.calcHist([hsv],[0],mask,[180],[0,180])
#归一化直方图，使其范围为0~255
cv2.normalize(hist,hist,0,255,cv2.NORM_MINMAX)
#设置初始跟踪窗口的位置和大小
track_window=(0,0, frame.shape[1], frame.shape[ 0 ])
#循环读取视频帧
while True:
    ret,frame = cap.read()
    if not ret:
        break
    #转换颜色空间
    hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #计算反向投影
    dst=cv2.calcBackProject([hsv],[0],hist,[0,180],1)
    #应用Camshitt算法进行目标跟踪
    ret,track_window= cv2.CamShift(dst, track_window, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,10,1))
    #获取旋转矩形的4个顶点
    pts = cv2.boxPoints(ret)
    pts= np.int0(pts)#在图像上绘制轮廓
    cv2.polylines(frame,[pts],True,255,2)
    #显示跟踪结果
    cv2.imshow('Track_ing',frame)
    #按'q'键退出循环
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
#释放视频资源并关闭窗口
cap.release()
cv2.destroyAllWindows()



