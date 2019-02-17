from part_05.settings import *
import pygame as pg
import math

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT / 2
        self.pos = self.rect.center
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.width = self.rect.width
        self.height = self.rect.height

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.vel.y = -22

    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION

        self.vel += self.acc
        self.pos += self.vel

        if abs(self.vel.x) < 0.5:
            self.vel.x = 0
        # if abs(self.vel.y) < 0.5:
        #     self.vel.y = 0

        print(self.vel.y)

        if self.rect.left > WIDTH:
            self.pos.x = 0 - self.width / 2
        if self.rect.right < 0:
            self.pos.x = WIDTH + self.width / 2

        # 防止碰撞后的0.5px的上下抖动
        # if math.fabs(self.rect.bottom - self.pos.y) >= 1:
        self.rect.bottom = self.pos.y
        self.rect.x = self.pos.x - self.width / 2


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
