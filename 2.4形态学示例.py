# import cv2
# # 读取图像  
# image = cv2.imread("C://Users//86159//Desktop//test.jpg", cv2.IMREAD_GRAYSCALE)
# # 创建结构元素,这里使用5x5的矩形

# kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
# #图像膨胀操作
# dilated_image = cv2.dilate(image,kernel,iterations =2)
# #图像腐蚀操作
# eroded_image=cv2.erode(image, kernel, iterations=2)
# #开运算
# opened_image =cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
# #闭运算
# closed_image =cv2.morphologyEx(image,cv2.MORPH_CLOSE, kernel)#显示结果
# cv2.imshow('Original',image)
# cv2.imshow('Dilated',dilated_image)
# cv2.imshow('Eroded',eroded_image)
# cv2.imshow('Opened',opened_image)
# cv2.imshow('Closed',closed_image)
# #等待用户按键退出
# cv2.waitKey(0)
# cv2.destroyAllWindows()


import cv2
import numpy as np

# 读取图像
image = cv2.imread("C://Users//86159//Desktop//test.jpg", cv2.IMREAD_GRAYSCALE)

# 创建结构元素，这里使用5x5的矩形
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# 图像膨胀操作
dilated_image = cv2.dilate(image, kernel, iterations=2)

# 图像腐蚀操作
eroded_image = cv2.erode(image, kernel, iterations=2)

# 开运算
opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# 闭运算
closed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

# 定义缩放比例，这里设置为 0.6 可以根据需要调整
scale_percent = 50
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

scale_percent1 = 60
width1 = int(image.shape[1] * scale_percent1 / 100)
height1 = int(image.shape[0] * scale_percent1 / 100)
dim1 = (width1, height1)

# 对除原始图像外的其他图像进行缩放
resize_origined_image = cv2.resize(image, dim1, interpolation=cv2.INTER_AREA)
resized_dilated_image = cv2.resize(dilated_image, dim, interpolation=cv2.INTER_AREA)
resized_eroded_image = cv2.resize(eroded_image, dim, interpolation=cv2.INTER_AREA)
resized_opened_image = cv2.resize(opened_image, dim, interpolation=cv2.INTER_AREA)
resized_closed_image = cv2.resize(closed_image, dim, interpolation=cv2.INTER_AREA)

# 创建一个空白的大图，采用 2x2 的布局
combined_image = np.zeros((height * 2 + 50, width * 2 + 50), dtype=np.uint8)

# 将膨胀图像复制到大图的左上角
combined_image[25:25 + height, 25:25 + width] = resized_dilated_image
# 添加标签
cv2.putText(combined_image, 'Dilated', (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)

# 将腐蚀图像复制到大图的右上角
combined_image[25:25 + height, 25 + width + 25:25 + width + 25 + width] = resized_eroded_image
# 添加标签
cv2.putText(combined_image, 'Eroded', (25 + width + 25, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)

# 将开运算图像复制到大图的左下角
combined_image[25 + height + 25:25 + height + 25 + height, 25:25 + width] = resized_opened_image
# 添加标签
cv2.putText(combined_image, 'Opened', (25, 25 + height + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)

# 将闭运算图像复制到大图的右下角
combined_image[25 + height + 25:25 + height + 25 + height, 25 + width + 25:25 + width + 25 + width] = resized_closed_image
# 添加标签
cv2.putText(combined_image, 'Closed', (25 + width + 25, 25 + height + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)

# 显示原始图像
cv2.imshow('Original', resize_origined_image)

# 显示拼接后的大图
cv2.imshow('Combined Images', combined_image)

# 等待用户按键退出
cv2.waitKey(0)
cv2.destroyAllWindows()