# https://opengameart.org/content/jumper-pack
from part_07.settings import *
import pygame as pg
import math
from xml.dom.minidom import parse

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image("bunny1_stand.png")
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
            self.vel.y = -PLAYER_JUMP

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

        if self.rect.left > WIDTH:
            self.pos.x = 0 - self.width / 2
        if self.rect.right < 0:
            self.pos.x = WIDTH + self.width / 2

        # 防止碰撞后的0.5px的上下抖动
        if math.fabs(self.rect.bottom - self.pos.y) >= 1:
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


class Spritesheet:
    def __init__(self, png_file_name, xml_file_name):
        self.sprite_sheet = pg.image.load(png_file_name)
        self.sprite_sheet_dom_tree = parse(xml_file_name)
        self.dic_image = {}
        self.root_textures = self.sprite_sheet_dom_tree.documentElement
        self.sub_textures = self.root_textures.getElementsByTagName("SubTexture")

    def get_image_rect(self, img_name):
        if self.dic_image.get(img_name):
            return self.dic_image[img_name]
        for texture in self.sub_textures:
            name = texture.getAttribute("name")
            if img_name == name:
                self.dic_image[img_name] = pg.Rect(
                    int(texture.getAttribute("x")),
                    int(texture.getAttribute("y")),
                    int(texture.getAttribute("width")),
                    int(texture.getAttribute("height"))
                )
                return self.dic_image[img_name]

    def get_image(self, img_name):
        rect = self.get_image_rect(img_name)
        image = pg.Surface((rect.width, rect.height))
        image.blit(self.sprite_sheet, (0, 0), rect)
        image = pg.transform.scale(image, (rect.width // 3, rect.height // 3))
        image.set_colorkey(BLACK, 1)
        return image
