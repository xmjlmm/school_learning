# import cv2
# import numpy as np
# fibe = cv2.imread("C://Users//86159//Desktop//test.jpg")
# rows,cols =fibe.shape[:2]#指定原始图像中的四边形顶点pts1
# #读取原图
# #获取图像的行数和列数
# print(rows,cols)
# pts1=np.float32([[650,50],[2600,60],[660,3450],[2700,3600]])
# #指定目标图像中的4个顶点pts2
# pts2=np.float32([[50,50],[rows-50,50],[50,cols-50],[rows-50,cols-50]])
# #生成转换矩阵M
# M= cv2.getPerspectiveTransform(pts1,pts2)#透视变换
# dst =cv2.warpPerspective(fibe,M,(cols,rows))
# cv2.namedWindow('Origin',cv2.WINDOW_NORMAL)
# cv2.namedWindow('Perspective',cv2.WINDOW_NORMAL,)
# cv2.imshow("Origin",fibe)
# cv2.imshow("Perspective",dst)
# cv2.waitKey()
# cv2.destroyAllWindows()






import cv2
import numpy as np

# 读取图像
fibe = cv2.imread("C://Users//86159//Desktop//test.jpg")
rows, cols = fibe.shape[:2]

# 打印图像的行数和列数
print(rows, cols)

# 指定原始图像中的四边形顶点 pts1
# 这里选择图像内部的一个四边形区域
pts1 = np.float32([[100, 100], [840, 100], [100, 840], [840, 840]])

# 指定目标图像中的 4 个顶点 pts2
# 选择图像的四个角点作为目标位置
pts2 = np.float32([[0, 0], [cols-200, 0], [0, rows-200], [cols-200, rows-200]])

# 生成转换矩阵 M
M = cv2.getPerspectiveTransform(pts1, pts2)

# 透视变换
dst = cv2.warpPerspective(fibe, M, (cols, rows))

# 创建可调整大小的窗口
cv2.namedWindow('Origin', cv2.WINDOW_NORMAL)
cv2.namedWindow('Perspective', cv2.WINDOW_NORMAL)

# 显示原始图像和透视变换后的图像
cv2.imshow("Origin", fibe)
cv2.imshow("Perspective", dst)

# 等待用户按键
cv2.waitKey()

# 关闭所有窗口
cv2.destroyAllWindows()




# import cv2
# import numpy as np

# # 读取图像
# fibe = cv2.imread("C://Users//86159//Desktop//test.jpg")
# rows, cols = fibe.shape[:2]

# # 打印图像的行数和列数
# print(rows, cols)

# # 指定原始图像中的四边形顶点 pts1
# # 这里选择图像内部的一个四边形区域
# pts1 = np.float32([[100, 100], [300, 100], [100, 300], [300, 300]])

# # 指定目标图像中的 4 个顶点 pts2
# # 让局部区域（这里是右侧）明显被拉伸
# pts2 = np.float32([[100, 100], [600, 100], [100, 300], [600, 300]])

# # 生成转换矩阵 M
# M = cv2.getPerspectiveTransform(pts1, pts2)

# # 透视变换
# dst = cv2.warpPerspective(fibe, M, (cols, rows))

# # 创建可调整大小的窗口
# cv2.namedWindow('Origin', cv2.WINDOW_NORMAL)
# cv2.namedWindow('Perspective', cv2.WINDOW_NORMAL)

# # 显示原始图像和透视变换后的图像
# cv2.imshow("Origin", fibe)
# cv2.imshow("Perspective", dst)

# # 等待用户按键
# cv2.waitKey()

# # 关闭所有窗口
# cv2.destroyAllWindows()