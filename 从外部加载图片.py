import pygame
import sys

pygame.init()
# 设置主窗口
screen = pygame.display.set_mode((400,400))
screen.fill('white')
# 设置窗口标题
pygame.display.set_caption('小舒彤')
# 加载图片
image_surface = pygame.image.load("F:\\ich liben dich\\eafccb89b328c9d87de499eedcb5011.jpg")
orig_image = image_surface.get_size()
print(orig_image)

target_size = (100, 100)
target_image = pygame.transform.scale(image_surface, target_size)
'''
image_surface.fill((0, 0, 255), rect=(100, 100, 100, 50), special_flags=0) 
这一行代码是在 image_surface 图像表面上填充一个矩形区域。
(0, 0, 255) 是 RGB 颜色值，表示填充的颜色为蓝色（红色值为0，绿色值为0，蓝色值为255）。
rect=(100, 100, 100, 50) 是矩形的位置和尺寸参数，依次为左上角坐标 (100, 100)，宽度 100，高度 50。
special_flags=0 是特殊标志，通常默认为0，表示没有特殊处理。
'''
target_image.fill((0, 0, 255), rect=(100, 100, 100, 50), special_flags=0)
'''image_surface.scroll(100, 60) 是将 image_surface 图像表面内容向右滚动 100 像素，向下滚动 60 像素。
第一个参数 100 表示水平方向的滚动距离。
第二个参数 60 表示垂直方向的滚动距离。'''
target_image.scroll(100, 200)  # 移动图片
target_image = pygame.transform.rotozoom(target_image, 325, 1.0)


image2_surface = pygame.image.load("F:\\ich liben dich\\fe2ed02b895c7673e7045063aeef7d4.jpg")
orig_image2 = image2_surface.get_size()
target_size2 = (100, 100)
target_image2 = pygame.transform.scale(image2_surface, target_size2)
target_image3 = pygame.transform.rotozoom(target_image2, 45, 1.0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # 将图像添加到主屏幕上
    screen.blit(target_image3, (0, 0))
    screen.blit(target_image, (100, 0))
    # pygame.Surface.blit(target_image2, target_image)
    # 更新屏幕内容
    pygame.display.flip()


