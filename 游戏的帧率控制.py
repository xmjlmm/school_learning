import pygame
pygame.init()
screen = pygame.display.set_mode((500, 400))
screen.fill((255, 255, 255))
pygame.display.set_caption('时间设置')
# 获取时间
t = pygame.time.get_ticks()
# 暂停游戏3000毫秒
t1 = pygame.time.wait(3000)
print(t1)
image_org = pygame.image.load("F:\\ich liben dich\\fe2ed02b895c7673e7045063aeef7d4.jpg")
image_surface = pygame.transform.rotozoom(image_org, 0, 0.2)
# 创建时间对象
clock = pygame.time.Clock()
while True:
    # 通过时间对象指定循环帧数，每秒循环60次
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        screen.blit(image_surface, (0, 0))
        pygame.display.update()
