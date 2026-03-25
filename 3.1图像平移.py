import cv2
import numpy as np
#读取原图
fibe = cv2. imread("C://Users//86159//Desktop//test.jpg")
#获取图像的高度和宽度
height,width = fibe. shape[ :2 ]
x = 150#向右移动150个像素
y = 200#向下移动200个像素
#转换矩阵M
M= np.float32([[1,0,x],[0,1,y]])
Panned_fibe = cv2.warpAffine(fibe,M,(width, height))
cv2.namedWindow('Origin', cv2.WINDOW_NORMAL)
cv2.namedWindow('Shift', cv2.WINDOW_NORMAL)
cv2.imshow("Origin",fibe)
cv2.imshow("Shift", Panned_fibe)
cv2.waitKey()
cv2.destroyAllWindows()
