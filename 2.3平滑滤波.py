# import cv2
# # 读取图像
# image = cv2.imread("C://Users//86159//Desktop//test.jpg", cv2.IMREAD_GRAYSCALE)
# # 均值滤波
# mean_filtered = cv2.blur(image,(3,3))
# # 中值滤波
# median_filtered = cv2.medianBlur(image,3)
# # 高斯滤波
# gaussian_filtered = cv2.GaussianBlur(image,(5,5),0)
# # 显示原始图像和滤波后的图像
# cv2.imshow('Original Image',image)
# cv2.imshow('Mean Filtered',mean_filtered)
# cv2.imshow('Median Filtered',median_filtered)
# cv2.imshow('Gaussian Filtered',gaussian_filtered)
# #等待用户按键退出
# cv2.waitKey(0)
# cv2.destroyAllWindows()



import cv2
import numpy as np

# 读取图像
image = cv2.imread("C://Users//86159//Desktop//test.jpg", cv2.IMREAD_GRAYSCALE)

# 均值滤波
mean_filtered = cv2.blur(image, (3, 3))

# 中值滤波
median_filtered = cv2.medianBlur(image, 3)

# 高斯滤波
gaussian_filtered = cv2.GaussianBlur(image, (5, 5), 0)

# 定义缩放比例，这里设置为 0.6 可以根据需要调整
scale_percent = 50
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)

# 对所有图像进行缩放
resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
resized_mean_filtered = cv2.resize(mean_filtered, dim, interpolation=cv2.INTER_AREA)
resized_median_filtered = cv2.resize(median_filtered, dim, interpolation=cv2.INTER_AREA)
resized_gaussian_filtered = cv2.resize(gaussian_filtered, dim, interpolation=cv2.INTER_AREA)

# 创建一个空白的大图
combined_image = np.zeros((height * 2 + 50, width * 2 + 50), dtype=np.uint8)

# 将原始图像复制到大图的左上角
combined_image[25:25 + height, 25:25 + width] = resized_image
# 添加标签
cv2.putText(combined_image, 'Original Image', (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)

# 将均值滤波后的图像复制到大图的右上角
combined_image[25:25 + height, 25 + width + 25:25 + width + 25 + width] = resized_mean_filtered
# 添加标签
cv2.putText(combined_image, 'Mean Filtered', (25 + width + 25, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)

# 将中值滤波后的图像复制到大图的左下角
combined_image[25 + height + 25:25 + height + 25 + height, 25:25 + width] = resized_median_filtered
# 添加标签
cv2.putText(combined_image, 'Median Filtered', (25, 25 + height + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)

# 将高斯滤波后的图像复制到大图的右下角
combined_image[25 + height + 25:25 + height + 25 + height, 25 + width + 25:25 + width + 25 + width] = resized_gaussian_filtered
# 添加标签
cv2.putText(combined_image, 'Gaussian Filtered', (25 + width + 25, 25 + height + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)

# 显示拼接后的大图
cv2.imshow('Combined Images', combined_image)

# 等待用户按键退出
cv2.waitKey(0)
cv2.destroyAllWindows()