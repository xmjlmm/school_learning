'''
一.Pygame程序基本搭建过程
Pygame搭建游戏窗口主要为如下几步

1.初始化化程序
在使用Pygame编程之前，我们要对程序进行初始化，代码如下
'''

import pygame
import sys

pygame.init()
# 也可以叫做screen对象，本质上是一个Surface对象
screen = pygame.display.set_mode((400, 400))
print(screen)

# 创建一个带文本的Surface对象
# text = font.render("小马哥不马虎",True,(255,255,255),(0,0,0))
# 准备要绘制的文本和位置
font = pygame.font.SysFont(None, 36)  # 使用系统默认字体，大小为36
text = "小马哥不马虎"
text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))  # 创建文本的 Surface 对象
text_rect = text_surface.get_rect()
text_rect.center = (200, 200)  # 设置文本位置为窗口中心

# 通过blit方法将其绘制出来，textRect表示位置坐标

# screen.blit(text_surface, text_rect)

# 加载图像
surface_image = pygame.image.load("F:\\ich liben dich\\fe2ed02b895c7673e7045063aeef7d4.jpg")
image_rect = surface_image.get_rect()
image_rect.center = (200, 100)  # 设置图像位置为窗口中心偏上

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # 填充背景色
    screen.fill((0, 0, 0))

    # 绘制文本
    screen.blit(text_surface, text_rect)

    # 绘制图像
    screen.blit(surface_image, image_rect)

    # 刷新屏幕
    pygame.display.flip()

