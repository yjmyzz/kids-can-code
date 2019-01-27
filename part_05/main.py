from part_05.sprites import *
from part_05.settings import *
import random


class Game:

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False

    def new(self):
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

        # 如果方块的高度<游戏屏幕高度的1/4,则所有档板下移(视觉上表现为整个屏幕向下滚动）
        if self.player.rect.top < HEIGHT / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.top += abs(self.player.vel.y)
                if plat.rect.top > HEIGHT:
                    # 同时为了提高性能，下移到屏幕之外的档板，清除掉(否则的话，仍然一直参与碰撞检测及渲染），游戏会越来越慢
                    plat.kill()

        # 由于下移到屏幕之外的档板被干掉，所以才继续源源不断的在上方随机补充新档板
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

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.debug()
        pg.display.flip()

    def debug(self):
        if DEBUG:
            font = pg.font.SysFont('Menlo', 25, True)
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
        pass

    def show_go_screen(self):
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
