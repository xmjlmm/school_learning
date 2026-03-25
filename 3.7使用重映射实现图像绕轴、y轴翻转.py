import cv2
import numpy as np
fibe = cv2.imread("C://Users//86159//Desktop//test.jpg")
#读取原图
rows,cols = fibe.shape[:2]
map1 = np.zeros(fibe.shape[:2],np.float32)
map2 = np.zeros(fibe.shape[:2],np.float32)#x、y坐标轴值交换
for i in range(rows):
    for j in range(cols):
        map1.itemset((i,j),cols-j-1)
        map2.itemset((i,j),rows-i-1)
rst = cv2.remap(fibe,map1,map2,cv2.INTER_LINEAR)
cv2.namedWindow('Origin',cv2.WINDOW_NORMAL)
cv2.namedWindow('Remap',cv2.WINDOW_NORMAL)
cv2.imshow("Origin",fibe)
cv2.imshow("Remap",rst)
cv2.waitKey()
cv2.destroyAllWindows()