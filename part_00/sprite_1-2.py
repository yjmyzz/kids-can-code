import pygame
from part_00.settings import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()


# 定义游戏主角类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # 第1行，必须调用Sprite父类的构造函数
        pygame.sprite.Sprite.__init__(self)
        # 注意：sprite必须指定image, rect这二个属性
        self.image = pygame.Surface((20, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT / 2

    # 更新逻辑
    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0


# 这里要有一个类似分组（或容器）的东西，存放所有游戏中的sprite实例
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    all_sprites.update()

    # draw /render
    screen.fill(BLACK)
    all_sprites.draw(screen)  # 绘制所有sprite

    pygame.display.update()

pygame.quit()
