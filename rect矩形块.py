import pygame
pygame.init()

screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption('小舒彤不书桐')
image_surface = pygame.image.load("F:\\ich liben dich\\fe2ed02b895c7673e7045063aeef7d4.jpg")

rect1 = pygame.Rect(50, 50, 100, 100)
# 在原图的基础上创建一个新的子图（surface对象）
image_child = image_surface.subsurface(rect1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    # 在屏幕上显示子图的区域
    screen.blit(image_child, (0, 0))
    pygame.display.update()
