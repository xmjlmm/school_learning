import cv2
import numpy as np
#读取原图#获取图像的行数、列数和色彩通道
fibe= cv2.imread("C://Users//86159//Desktop//test.jpg")
rows, cols, ch =fibe.shape
pl=np.float32([[0,0],[cols-1, 0],[0,rows-1]])
p2=np.float32([[0,rows*0.33],[cols*0.85,rows *0.25],[cols * 0.15, rows * 0.7]])
M=cv2.getAffineTransform(pl,p2)#转换矩阵M
dst=cv2.warpAffine(fibe, M,(cols, rows))#按照指定点的关系计算确定所有其
cv2.namedWindow('Origin',cv2.WINDOW_NORMAL)
cv2.namedWindow('Affine', cv2. WINDOW_NORMAL)
cv2.imshow("Origin", fibe)
cv2.imshow("Affine", dst)
cv2.waitKey()
cv2.destroyAllWindows( )