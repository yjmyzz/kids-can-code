from part_14.sprites import *
from part_14.settings import *
import random
from os import path


class Game:

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False
        self.font_name = FONT_NAME
        self.high_score = 0
        self.score = 0
        self.dir = path.dirname(__file__)
        self.load_data()

    def load_data(self):
        file_path = path.join(self.dir, HIGH_SCORE_FILE)
        if path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    self.high_score = int(f.read())
                except:
                    self.high_score = 0
        self.spritesheet = Spritesheet(path.join(self.dir, SPRITE_SHEET_PNG_FILE),
                                       path.join(self.dir, SPRITE_SHEET_XML_FILE))

        # 设置声音目录
        # 声音素材，可通过https://www.bfxr.net/获取
        self.snd_dir = path.join(self.dir, "../snd")
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, "Jump.wav"))

    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            if p.rect.right >= WIDTH:
                p.rect.centerx = p.rect.centerx - (p.rect.right - WIDTH) - 2
            self.all_sprites.add(p)
            self.platforms.add(p)
        # 加载背景音乐
        pg.mixer.music.load(path.join(self.snd_dir, "bgm.mp3"))
        self.run()

    def run(self):
        # 循环播放背景音乐
        pg.mixer.music.play(-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        # game over时背景音乐淡出
        pg.mixer.music.fadeout(500)

    def update(self):
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.bottom:
                    if lowest.rect.right + 5 >= self.player.rect.centerx >= lowest.rect.left - 5:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        if self.player.rect.top < HEIGHT / 4:

            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.top += max(abs(self.player.vel.y), 2)
                if plat.rect.top > HEIGHT:
                    plat.kill()
                    self.score += 10

        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.top -= max(self.player.vel.y, 5)
                if sprite.rect.bottom < 0:
                    sprite.kill()
            if len(self.platforms) <= 0:
                self.playing = False

        while len(self.platforms) <= 5 and self.player.rect.bottom < HEIGHT:
            width = random.randrange(50, 100)
            p = Platform(self, random.randint(0, WIDTH - width),
                         random.randint(-70, -30))
            if p.rect.right >= WIDTH:
                p.rect.centerx = p.rect.centerx - (p.rect.right - WIDTH) - 2
            self.all_sprites.add(p)
            hits = pg.sprite.spritecollide(p, self.platforms, False)
            if hits:
                p.kill()
            else:
                self.platforms.add(p)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def debug(self):
        if DEBUG:
            font = pg.font.SysFont(self.font_name, 25, True)
            pos_txt = font.render(
                'Pos:(' + str(round(self.player.pos.x, 2)) + "," + str(round(self.player.pos.y, 2)) + ")", 1, GREEN)
            vel_txt = font.render(
                'Vel:(' + str(round(self.player.vel.x, 2)) + "," + str(round(self.player.vel.y, 2)) + ")", 1, GREEN)
            acc_txt = font.render(
                'Acc:(' + str(round(self.player.acc.x, 2)) + "," + str(round(self.player.acc.y, 2)) + ")", 1, GREEN)
            self.screen.blit(pos_txt, (20, 10))
            self.screen.blit(vel_txt, (20, 40))
            self.screen.blit(acc_txt, (20, 70))
            pg.draw.line(self.screen, WHITE, (0, HEIGHT / 2), (WIDTH, HEIGHT / 2), 1)
            pg.draw.line(self.screen, WHITE, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT), 1)

    def show_start_screen(self):
        # 启动界面播放背景音乐
        pg.mixer.music.load(path.join(self.snd_dir, "start_and_go.ogg"))
        pg.mixer.music.play(-1)
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT * 0.4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT * 0.55)
        self.draw_text("Press a key to play", 20, WHITE, WIDTH / 2, HEIGHT * 0.7)
        self.draw_text("High Score: " + str(self.high_score), 20, WHITE, WIDTH / 2, 15)
        pg.display.update()
        self.wait_for_key()
        # 有按键开始时，淡出背景音
        pg.mixer.music.fadeout(500)

    def draw(self):
        self.screen.fill(LIGHT_BLUE)
        self.all_sprites.draw(self.screen)
        self.debug()
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        self.screen.blit(self.player.image, self.player.rect)
        pg.display.update()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def show_go_screen(self):
        # 启动界面播放背景音乐
        pg.mixer.music.load(path.join(self.snd_dir, "start_and_go.ogg"))
        pg.mixer.music.play(-1)
        self.screen.fill(BG_COLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT * 0.4)
        self.draw_text("Score:  " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT * 0.55)
        self.draw_text("Press a key to play again", 20, WHITE, WIDTH / 2, HEIGHT * 0.7)
        if self.score > self.high_score:
            self.high_score = self.score
            self.draw_text("New High Score: " + str(self.high_score), 28, WHITE, WIDTH / 2, 25)
            with open(path.join(self.dir, HIGH_SCORE_FILE), "w") as f:
                f.write(str(self.high_score))
        else:
            self.draw_text("High Score: " + str(self.high_score), 20, WHITE, WIDTH / 2, 15)

        pg.display.update()
        self.wait_for_key()
        # 有按键开始时，淡出背景音
        pg.mixer.music.fadeout(500)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.SysFont(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
