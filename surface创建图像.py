# import pygame
# import sys
#
# pygame.init()
# # 设置主窗口
# screen = pygame.display.set_mode((400, 400))
# screen.fill('blue')
# # 设置窗口标题
# pygame.display.set_caption('小舒彤不书桐')
# # 创建一个图像
# face = pygame.Surface((60, 60), flags = pygame.HWSURFACE)
# # 填充图像
# face.fill(color='pink')
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     # 将图像添加到主屏幕上
#     screen.blit(face, (100, 100))
#     # 更新屏幕内容
#     pygame.display.flip()


# import pygame
# import sys
#
# pygame.init()
#
# # 设置主窗口
# screen = pygame.display.set_mode((400, 400))
# screen.fill('blue')
#
# # 设置窗口标题
# pygame.display.set_caption('书桐不舒彤')
#
# # 加载图片
# image_path = "F:\\ich liben dich\\fe2ed02b895c7673e7045063aeef7d4.jpg"
# face_orig = pygame.image.load(image_path)
#
# # 获取图片原始大小
# original_size = face_orig.get_size()
# print("原始图片大小：", original_size)
#
# # 缩放图片
# target_size = (400, 400)
# face = pygame.transform.scale(face_orig, target_size)
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#     # 将缩放后的图片绘制到主屏幕上
#     screen.blit(face, (0, 0))
#
#     # 更新屏幕内容
#     pygame.display.flip()

# 导入pygame和sys模块
import pygame
import sys

# 初始化pygame
pygame.init()

# 创建一个窗口
screen = pygame.display.set_mode((400, 400))

# 设置窗口颜色
screen.fill('purple')

# 设置窗口颜色
pygame.display.set_caption('书桐不舒彤')

# 加载图片
image_source = 'F:\\ich liben dich\\fe2ed02b895c7673e7045063aeef7d4.jpg'
image_face = pygame.image.load(image_source)

# 获取图片原始大小
org_image = image_face.get_size()
print(org_image)

# 压缩图片大小，适应窗口
target_size = (400, 400)
tar_image = pygame.transform.scale(image_face, target_size)

# 老套路
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(tar_image, (0, 0))

    pygame.display.flip()







