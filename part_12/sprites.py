# https://opengameart.org/content/jumper-pack
from part_12.settings import *
import pygame as pg
import math
from xml.dom.minidom import parse

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        # 行走状态
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]

        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT / 2
        self.pos = self.rect.center
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.width = self.rect.width
        self.height = self.rect.height

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image("bunny1_ready.png"),
                                self.game.spritesheet.get_image("bunny1_stand.png")]
        self.walking_frames_right = [self.game.spritesheet.get_image("bunny1_walk1.png"),
                                     self.game.spritesheet.get_image("bunny1_walk2.png")]
        self.walking_frames_left = []
        for frame in self.walking_frames_right:
            self.walking_frames_left.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image("bunny1_jump.png")

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
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

        if self.rect.left > WIDTH:
            self.pos.x = 0 - self.width / 2
        if self.rect.right < 0:
            self.pos.x = WIDTH + self.width / 2

        # 防止碰撞后的0.5px的上下抖动
        if math.fabs(self.rect.bottom - self.pos.y) >= 1:
            self.rect.bottom = self.pos.y
        self.rect.x = self.pos.x - self.width / 2

    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if self.walking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame += 1
                bottom = self.rect.bottom
                if self.vel.x < 0:
                    self.image = self.walking_frames_left[self.current_frame % len(self.walking_frames_left)]
                elif self.vel.x > 0:
                    self.image = self.walking_frames_right[self.current_frame % len(self.walking_frames_right)]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame += 1
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame % len(self.standing_frames)]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.game = game
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
