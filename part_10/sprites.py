# https://opengameart.org/content/jumper-pack
from part_10.settings import *
import pygame as pg
from xml.dom.minidom import parse

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        # 是否在行走状态
        self.walking = False
        # 是否处于跳跃状态
        self.jumping = False
        # 当前状态的动画，显示的是哪一"帧"
        self.current_frame = 0
        # 当前状态的动画，最后一次切换是什么时候？
        self.last_update = 0
        # 加载图片
        self.load_images()
        # 初始状态为"站立"
        self.image = self.standing_frames[0]

        self.rect = self.image.get_rect()
        self.rect.center = WIDTH / 2, HEIGHT / 2
        self.pos = self.rect.center
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.width = self.rect.width
        self.height = self.rect.height

    # 加载各种状态的图片序列
    def load_images(self):
        # 站立状态的图片
        self.standing_frames = [self.game.spritesheet.get_image("bunny1_ready.png"),
                                self.game.spritesheet.get_image("bunny1_stand.png")]

        # 向右走的图片
        self.walking_frames_right = [self.game.spritesheet.get_image("bunny1_walk1.png"),
                                     self.game.spritesheet.get_image("bunny1_walk2.png")]

        # 向左走的图片
        self.walking_frames_left = []
        for frame in self.walking_frames_right:
            # 向左走的图片，只需要把向"右"走的图片，水平(x)方向翻转即可
            self.walking_frames_left.append(pg.transform.flip(frame, True, False))

        # 跳跃状态的图片
        self.jump_frame = self.game.spritesheet.get_image("bunny1_jump.png")

    def jump(self):
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            self.vel.y = -PLAYER_JUMP
            # 修改跳跃状态
            self.jumping = True

    def update(self):
        # 动画处理
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

        # 因为walking状态的切换，依赖于x速度是否为0判断，当x在0左右的极小值摆动时，会导致判断出错
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

        if self.rect.left > WIDTH:
            self.pos.x = 0 - self.width / 2
        if self.rect.right < 0:
            self.pos.x = WIDTH + self.width / 2

        if abs(self.rect.bottom - self.pos.y) >= 1:
            self.rect.bottom = self.pos.y
        self.rect.x = self.pos.x - self.width / 2

    # 动画处理
    def animate(self):
        now = pg.time.get_ticks()

        # 更新walking状态
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # 垂直方向速度为0，认为未跳跃
        if abs(self.vel.y) < 0.5:
            self.jumping = False

        # 切换jumping图片
        if self.jumping:
            self.image = self.jump_frame
        else:
            self.image = self.standing_frames[0]

        if not self.jumping and not self.walking:
            # 调节这里的200,可以控制动画的播放速度
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame += 1
                # bunny1_ready.png与bunny1_stand.png的高度不同，所以切换后，要调整bottom值，保证图片的最下边缘正好站在档板上
                old_bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame % len(self.standing_frames)]
                self.rect = self.image.get_rect()
                self.rect.bottom = old_bottom


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
