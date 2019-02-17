from part_10.sprites import *
from part_10.settings import *
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
        # 加载历史最高分
        file_path = path.join(self.dir, HIGH_SCORE_FILE)
        if path.exists(file_path):
            with open(file_path, "r") as f:
                try:
                    self.high_score = int(f.read())
                except:
                    self.high_score = 0
        # load spritesheet
        self.spritesheet = Spritesheet(path.join(self.dir, SPRITE_SHEET_PNG_FILE),
                                       path.join(self.dir, SPRITE_SHEET_XML_FILE))

    def new(self):
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)

        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        if self.player.rect.top < HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.top += abs(self.player.vel.y)
                if plat.rect.top > HEIGHT:
                    plat.kill()
                    # 得分+10
                    self.score += 10
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.top -= max(self.player.vel.y, 5)
                if sprite.rect.bottom < 0:
                    sprite.kill()
            if len(self.platforms) <= 0:
                self.playing = False

        while len(self.platforms) <= 5:
            width = random.randint(50, 100)
            p = Platform(random.randint(0, WIDTH - width),
                         random.randint(-70, -30),
                         width, 10)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

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
        self.screen.fill(BG_COLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT * 0.4)
        self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT * 0.55)
        self.draw_text("Press a key to play", 20, WHITE, WIDTH / 2, HEIGHT * 0.7)
        self.draw_text("High Score: " + str(self.high_score), 20, WHITE, WIDTH / 2, 15)
        pg.display.update()
        self.wait_for_key()

    def draw(self):
        self.screen.fill(LIGHT_BLUE)
        self.all_sprites.draw(self.screen)
        self.debug()
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()

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
        self.screen.fill(BG_COLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT * 0.4)
        self.draw_text("Score:  " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT * 0.55)
        self.draw_text("Press a key to play again", 20, WHITE, WIDTH / 2, HEIGHT * 0.7)
        # 如果得分出现新记录，保存下来
        if self.score > self.high_score:
            self.high_score = self.score
            self.draw_text("New High Score: " + str(self.high_score), 28, WHITE, WIDTH / 2, 25)
            with open(path.join(self.dir, HIGH_SCORE_FILE), "w") as f:
                f.write(str(self.high_score))
        else:
            self.draw_text("High Score: " + str(self.high_score), 20, WHITE, WIDTH / 2, 15)

        pg.display.update()
        self.wait_for_key()

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
