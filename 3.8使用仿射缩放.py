import cv2
import numpy as np
fibe = cv2.imread("C://Users//86159//Desktop//test.jpg")
#读取原图
height,width,channel = fibe.shape
#x轴焦距的0.1倍
w = 0.1
#y轴焦距的0.05倍
h = 0.05
#声明变换矩阵M:w、h为缩放系数,平移系数为0
M=np.float32([[w,0,0],[0,h,0]])
#进行仿射变换
resized = cv2. warpAffine(fibe, M, (int(width* w),int(height * h)))
cv2.imwrite('resize.jpg',resized)
cv2.namedWindow('Origin',cv2.WINDOW_NORMAL)
cv2.namedWindow('Resize',cv2.WINDOW_NORMAL)
cv2.imshow("Origin",fibe)
cv2.imshow("Resize",resized)
cv2.waitKey()
cv2.destroyAllWindows( )