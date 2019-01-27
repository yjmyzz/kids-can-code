from part_04.sprites import *
from part_04.settings import *
import sys


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
