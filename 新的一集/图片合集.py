import cv2
import time

# 图片文件路径，这里请替换为你实际的图片路径
image_path = "F:\\photo\\1\\1.jpg"

# 读取图片
img = cv2.imread(image_path)

# 检查图片是否成功读取
if img is None:
    print("无法读取图片，请检查图片路径是否正确")
else:
    # 显示图片，窗口标题为'Image'，可以根据需求修改
    cv2.imshow('Image', img)
    # 等待10秒（10000毫秒）
    cv2.waitKey(10000)
    # 关闭所有窗口
    cv2.destroyAllWindows()