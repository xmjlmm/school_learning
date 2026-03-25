import cv2
#读取图像
image =cv2.imread("C://Users//86159//Desktop//test.jpg")
#将图像转换为 HSV 色彩空间
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)#分离HSV图像的各个通道
h, s, v=cv2.split(hsv_image)#对V通道进行直方图均衡化
equ_v=cv2.equalizeHist(v)
#合并均衡化后的V通道回到HSV图像
hsv_image_eq = cv2.merge([h,s,equ_v])
#将均衡化后的HSV图像转换回BGR色彩空间
bgr_image_eq = cv2.cvtColor(hsv_image_eq, cv2.COLOR_HSV2BGR)
#显示原始图像和均衡化后的图像
cv2.imshow('Original Image',image)
cv2.imshow('Equalized Image',bgr_image_eq)
#等待用户按键退出
cv2.waitKey(0)
cv2.destroyAl1Windows()