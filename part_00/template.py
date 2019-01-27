import pygame
import time

# 游戏中的一些常量定义
SIZE = WIDTH, HEIGHT = 300, 100
FPS = 10

# 颜色常量定义
BLACK = 0, 0, 0
WHITE = 255, 255, 255

# 初始化
pygame.init()
pygame.mixer.init()

# 窗口、标题等初始化
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# 循环入口
running = True
while running:

    # 设置帧数
    clock.tick(FPS)

    # 事件处理
    for event in pygame.event.get():
        # 退出处理
        if event.type == pygame.QUIT:
            running = False

    # (update) 游戏更新逻辑(比如：改动角色的位置或一些重要变量等，这里仅演示更新当前时间)
    font = pygame.font.SysFont('Menlo', 25, True)
    current_time = font.render(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), 1, WHITE)

    # (draw)渲染屏幕
    screen.fill(BLACK)  # 先准备一块黑布
    screen.blit(current_time, current_time.get_rect(center=(WIDTH / 2, HEIGHT / 2)))  # 把时间显示在画布中央

    # 屏幕内容刷新
    pygame.display.update()

# 循环结束后，退出游戏
pygame.quit()
