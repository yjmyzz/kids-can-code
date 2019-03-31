# https://opengameart.org/content/jumper-pack
from part_18.settings import *
import pygame as pg
import math
from xml.dom.minidom import parse
import random

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (35, HEIGHT - 35)
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

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.vel.y = -PLAYER_JUMP
            if abs(self.vel.x) < 0.5:
                self.jumping = True

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

        if abs(self.vel.y) < 0.5:
            self.vel.y = 0

        if self.rect.left > WIDTH:
            self.pos.x = 0 - self.width / 2
        if self.rect.right < 0:
            self.pos.x = WIDTH + self.width / 2

        if math.fabs(self.rect.bottom - self.pos.y) >= 1:
            self.rect.bottom = self.pos.y
        self.rect.x = self.pos.x - self.width / 2

    def animate(self):
        now = pg.time.get_ticks()

        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        if abs(self.vel.y) < 0.5:
            self.jumping = False

        if self.jumping:
            self.image = self.jump_frame

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

        # 加上mask
        self.mask = pg.mask.from_surface(self.image)


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images = [self.game.spritesheet.get_image("ground_grass_broken.png"),
                  self.game.spritesheet.get_image("ground_grass_small_broken.png")]
        self.image = random.choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < BOOST_POWER_PERCENT:
            power = PowerUp(self.game, self)
            self.game.all_sprites.add(power, layer=POWERUP_LAYER)
            self.game.powerups.add(power)


class Cloud(pg.sprite.Sprite):
    def __init__(self, game, x, y, scale=1):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = self.game.spritesheet.get_image("cloud.png", scale)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, plat):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.plat = plat
        self.current_frame = 0
        self.last_update = 0
        # 换成金币效果
        self.images = [self.game.spritesheet.get_image("gold_1.png"),
                       self.game.spritesheet.get_image("gold_2.png"),
                       self.game.spritesheet.get_image("gold_3.png"),
                       self.game.spritesheet.get_image("gold_4.png")]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 3

    def update(self):
        self.animate()
        self.rect.bottom = self.plat.rect.top - 3
        if not self.game.platforms.has(self.plat):
            self.kill()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 200:
            self.last_update = now
            self.current_frame += 1
            self.image = self.images[self.current_frame % len(self.images)]
            self.rect = self.image.get_rect()
            self.rect.bottom = self.plat.rect.top - 3
            self.rect.centerx = self.plat.rect.centerx


class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.current_frame = 0
        self.last_update = 0
        self.image_up = self.game.spritesheet.get_image("flyMan_fly.png")
        self.image_down = self.game.spritesheet.get_image("flyMan_jump.png")
        self.image = self.image_up
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([-100, WIDTH + 100])
        self.vx = random.randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = random.randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if abs(self.vy) > 3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        # 加上mask
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()


class Spritesheet:
    def __init__(self, png_file_name, xml_file_name):
        self.sprite_sheet = pg.image.load(png_file_name).convert_alpha()
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

    def get_image(self, img_name, scale=3):
        rect = self.get_image_rect(img_name)
        image = pg.Surface((rect.width, rect.height)).convert()
        image.blit(self.sprite_sheet, (0, 0), rect)
        image = pg.transform.scale(image, (int(rect.width // scale), int(rect.height // scale)))
        image.set_colorkey(BLACK)
        return image
