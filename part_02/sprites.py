from part_02.settings import *
import pygame as pg

# Vector可以看成(x,y)的封装
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT / 2
        self.pos = self.rect.center
        # 速度
        self.vel = vec(0, 0)
        # 加速度
        self.acc = vec(0, 0)
        self.width = self.rect.width
        self.height = self.rect.height

    def update(self):
        # 每帧更新前，先初始化加速度为0
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            # 按左键时，减速
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            # 按右键时，加速
            self.acc.x = PLAYER_ACC

        # 加速(或减速）时，加入摩擦系数
        self.acc += self.vel * PLAYER_FRICTION

        # 将加速度，作用到速度上
        self.vel += self.acc

        # 更新sprite在屏幕上的位置
        self.pos += self.vel

        # 边界处理
        if self.rect.left > WIDTH:
            self.pos.x = 0 - self.width / 2
        if self.rect.right < 0:
            self.pos.x = WIDTH + self.width / 2

        # 更新rect到新的位置
        self.rect.center = self.pos
