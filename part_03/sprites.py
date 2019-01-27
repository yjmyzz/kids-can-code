from part_03.settings import *
import pygame as pg

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT / 2
        self.pos = self.rect.center
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.width = self.rect.width
        self.height = self.rect.height

    def update(self):
        # 初始化时，垂直方向加入重力加速度
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION

        self.vel += self.acc
        self.pos += self.vel

        if self.rect.left > WIDTH:
            self.pos.x = 0 - self.width / 2
        if self.rect.right < 0:
            self.pos.x = WIDTH + self.width / 2

        self.rect.midbottom = self.pos
        # 校正0.5px上下抖动的问题
        # if abs(self.rect.bottom - self.pos.y) >= 1:
        #     self.rect.bottom = self.pos.y
        # self.rect.x = self.pos.x - self.width / 2


# 档板类
class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
