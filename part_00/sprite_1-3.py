import pygame
from part_00.settings import *
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "../img/")


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder, "p1_jump.png"))
        # 如果图片显示时，发现不透明(看具体操作系统)，可以加下面这行
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT / 2
        self.y_speed = 5

    def update(self):
        self.rect.x += 5
        self.rect.y += self.y_speed

        # 边界检测
        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.top < PLAYER_TOP_LIMIT:
            self.y_speed = -self.y_speed
        if self.rect.bottom > PLAYER_BOTTOM_LIMIT:
            self.y_speed = -self.y_speed


all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

running = True
while running:

    clock.tick(FPS)

    # process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # draw /render
    screen.fill(BLACK)
    pygame.draw.line(screen, GREEN, (0, PLAYER_TOP_LIMIT), (WIDTH, PLAYER_TOP_LIMIT), 1)
    pygame.draw.line(screen, GREEN, (0, PLAYER_BOTTOM_LIMIT), (WIDTH, PLAYER_BOTTOM_LIMIT), 1)
    all_sprites.draw(screen)

    pygame.display.update()

pygame.quit()
