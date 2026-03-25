import pygame

pygame.init()

screen = pygame.display.set_mode((500,400))
pygame.display.set_caption('时间设置')
# 获取时间
t = pygame.time.get_ticks()
# 暂停游戏3000毫秒
t1 = pygame.time.wait(3000)
print(t1)

image_source = "F:\\ich liben dich\\fe2ed02b895c7673e7045063aeef7d4.jpg"
org_image = pygame.image.load(image_source)
target_size = (500, 400)
org_size = org_image.get_size()
target_image = pygame.transform.smoothscale(org_image, target_size)
image_surface = pygame.display.set_mode(target_size)
image_surface.blit(target_image, (0, 0))
pygame.display.flip()

# 定义自定义事件类型
UPDATE_EVENT = pygame.USEREVENT + 1

# 设置定时器，每隔1000毫秒触发一次UPDATE_EVENT事件
print(pygame.time.set_timer(UPDATE_EVENT, 1000)) # 这个定时器好像有一点点垃圾

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        screen.blit(image_surface, (0, 0))
        pygame.display.update()
