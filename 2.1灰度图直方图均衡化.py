import cv2
#读取图像
image = cv2.imread("C://Users//86159//Desktop//test.jpg", cv2.IMREAD_GRAYSCALE)
#进行直方图均衡化
equ_image=cv2.equalizeHist(image)
#显示原始图像和均衡化后的图像
cv2.imshow('Original Image',image)
cv2.imshow('Equalized Image',equ_image)
#等待用户按键退出
cv2.waitKey(0)
cv2.destroyAllWindows( )