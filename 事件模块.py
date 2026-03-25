# import pygame
# import sys
#
# # 初始化 Pygame
# pygame.init()
#
# # 设置屏幕大小和标题
# screen_width, screen_height = 400, 300
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption('事件处理示例')
#
# # 定义颜色
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
#
# # 设置字体
# font = pygame.font.Font(None, 36)
#
# # 初始化计数器
# counter = 0
#
# # 主循环
# running = True
# while running:
#     # 处理事件
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False  # 退出主循环
#             pygame.quit()  # 退出 Pygame
#             sys.exit()
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             # 鼠标按下事件：增加计数器
#             counter += 1
#             print(f'点击次数：{counter}')
#
#     # 填充白色背景
#     screen.fill(WHITE)
#
#     # 绘制文本到屏幕上
#     text = font.render(f'点击次数：{counter}', True, BLACK)
#     text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
#     screen.blit(text, text_rect)
#
#     # 更新屏幕显示
#     pygame.display.flip()
#
#     # 控制帧率
#     pygame.time.Clock().tick(10)
#


import pygame
import sys

# 初始化Pygame
pygame.init()

# 设置屏幕大小和标题
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('鼠标事件示例')

# 颜色定义
白色 = (255, 255, 255)
红色 = (255, 0, 0)
绿色 = (0, 255, 0)
蓝色 = (0, 0, 255)

# 字体设置
font_file = r"c:\windows\fonts\SimSun.ttc"
font = pygame.font.Font(font_file, 36)

# 文本位置
text_pos = (20, 20)

# 初始化计数器
click_counter = 0

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # 点击窗口关闭按钮退出程序
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                click_counter += 1
                print(f'左键点击：{click_counter}')
            elif event.button == 3:  # 右键点击
                print('右键点击')
            elif event.button == 2:  # 中键点击
                print('中键点击')
        elif event.type == pygame.MOUSEMOTION:
            # 获取鼠标当前位置
            mouse_x, mouse_y = event.pos
            print(f'鼠标移动到 ({mouse_x}, {mouse_y})')

    # 清空屏幕
    screen.fill(白色)

    # 显示点击次数
    click_text = font.render(f'点击次数: {click_counter}', True, 红色)
    screen.blit(click_text, text_pos)

    # 绘制鼠标当前位置（确保鼠标事件处理循环中定义了 mouse_x 和 mouse_y）
    if 'mouse_x' in locals() and 'mouse_y' in locals():
        pygame.draw.circle(screen, 绿色, (mouse_x, mouse_y), 5)

    # 更新屏幕显示
    pygame.display.flip()

    # 控制帧率
    pygame.time.Clock().tick(10000000000000000000000)  # 帧率越大，它越灵敏，反应越快，帧率越小，他就很卡，卡的话，反应就很缓慢

