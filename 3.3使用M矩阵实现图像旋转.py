# import cv2
# import numpy as np
# from math import cos, sin, radians
# img = cv2.imread("C://Users//86159//Desktop//test.jpg")
# height,width,channel=img.shape
# theta = 45
# def getRotationMatrix2D(angle,tx=0,ty=0):
#     #将角度值转换为弧度值#因为图像的左上角是原点,需要x(-1)
#     angle = radians(-1*angle)
#     M = np.float32([
#         [cos(angle),-sin(angle),(1-cos(angle))*tx+sin(angle)*ty],
#         [sin(angle),cos(angle),-sin(angle)*tx+(1-cos(angle))*ty]])
#     return M
# #求得图像中心点,作为旋转的轴心
# cx = int(width/2)
# cy = int(height/2)
# #进行 2D 仿射变换
# #围绕原点逆时针旋转 30°
# M = getRotationMatrix2D(30,tx=cx,ty=cy)
# rotated_30=cv2.warpAffine(img,M,(width, height))
# #围绕原点逆时针旋转45°
# M = getRotationMatrix2D(45,tx=cx,ty=cy)
# rotated_45 =cv2.warpAffine(img,M,(width, height))
# #围绕原点逆时针旋转60°
# M = getRotationMatrix2D(60,tx=cx,ty=cy)
# rotated_60=cv2.warpAffine(img,M,(width, height))
# cv2.namedWindow('Origin',cv2.WINDOW_NORMAL)
# cv2.namedWindow('Rotated 30 Degree', cv2.WINDOW_NORMAL)
# cv2.imshow("Origin",img)
# cv2.imshow("Rotated 30 Deqree",rotated_30[:,:,::-1])
# cv2.namedWindow('Rotated 45 Degree',cv2. WINDOW_NORMAL)
# cv2.imshow("Rotated 45 Degree",rotated_45[:,:,::-1])
# cv2.namedWindow('Rotated 60 Deqree',cv2.WINDOW_NORMAL)
# cv2.imshow("Rotated 60 Degree",rotated_60[:,:,::-1])
# cv2.waitKey()
# cv2.destroyAllWindows()



import cv2
import numpy as np
from math import cos, sin, radians

# 读取图像
img = cv2.imread("C://Users//86159//Desktop//test.jpg")
height, width, channel = img.shape

# 定义旋转角度
theta = 45

# 定义获取旋转矩阵的函数
def getRotationMatrix2D(angle, tx=0, ty=0):
    # 将角度值转换为弧度值，因为图像的左上角是原点，需要 x(-1)
    angle = radians(-1 * angle)
    # 计算旋转矩阵
    M = np.float32([
        [cos(angle), -sin(angle), (1 - cos(angle)) * tx + sin(angle) * ty],
        [sin(angle), cos(angle), -sin(angle) * tx + (1 - cos(angle)) * ty]
    ])
    return M

# 求得图像中心点，作为旋转的轴心
cx = int(width / 2)
cy = int(height / 2)

# 进行 2D 仿射变换
# 围绕原点逆时针旋转 30°
M = getRotationMatrix2D(30, tx=cx, ty=cy)
rotated_30 = cv2.warpAffine(img, M, (width, height))

# 围绕原点逆时针旋转 45°
M = getRotationMatrix2D(45, tx=cx, ty=cy)
rotated_45 = cv2.warpAffine(img, M, (width, height))

# 围绕原点逆时针旋转 60°
M = getRotationMatrix2D(60, tx=cx, ty=cy)
rotated_60 = cv2.warpAffine(img, M, (width, height))

# 定义缩放比例
scale_percent = 60
new_width = int(width * scale_percent / 100)
new_height = int(height * scale_percent / 100)
dim = (new_width, new_height)

# 对所有图像进行缩放
resized_original = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
resized_rotated_30 = cv2.resize(rotated_30, dim, interpolation=cv2.INTER_AREA)
resized_rotated_45 = cv2.resize(rotated_45, dim, interpolation=cv2.INTER_AREA)
resized_rotated_60 = cv2.resize(rotated_60, dim, interpolation=cv2.INTER_AREA)

# 创建一个空白的大图
combined_image = np.zeros((new_height * 2 + 50, new_width * 2 + 50, 3), dtype=np.uint8)

# 定义添加图像和标签的函数
def add_image_with_label(dest_img, src_img, x, y, label):
    dest_img[y:y + new_height, x:x + new_width] = src_img
    cv2.putText(dest_img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

# 将原始图像复制到大图的左上角
add_image_with_label(combined_image, resized_original, 25, 25, 'Original')

# 将旋转 30° 的图像复制到大图的右上角
add_image_with_label(combined_image, resized_rotated_30, 25 + new_width + 25, 25, 'Rotated 30 Degree')

# 将旋转 45° 的图像复制到大图的左下角
add_image_with_label(combined_image, resized_rotated_45, 25, 25 + new_height + 25, 'Rotated 45 Degree')

# 将旋转 60° 的图像复制到大图的右下角
add_image_with_label(combined_image, resized_rotated_60, 25 + new_width + 25, 25 + new_height + 25, 'Rotated 60 Degree')

# 显示拼接后的大图
cv2.namedWindow('Combined Images', cv2.WINDOW_NORMAL)
cv2.imshow('Combined Images', combined_image)

# 等待用户按键退出
cv2.waitKey(0)
cv2.destroyAllWindows()