from part_03.sprites import *
from part_03.settings import *


class Game:

    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False
        self.p1 = object

    def new(self):
        self.all_sprites = pg.sprite.Group()
        # 创建一个档板Group
        self.platforms = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        # 加入2个档板实例
        self.p1 = Platform(0, HEIGHT - 40, WIDTH, 40)
        p2 = Platform(WIDTH / 2 - 50, HEIGHT / 2 + 100, 100, 20)
        self.all_sprites.add(self.p1)
        self.all_sprites.add(p2)
        self.platforms.add(self.p1)
        self.platforms.add(p2)
        g.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        # 碰撞检测
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.pos.y = hits[0].rect.top
            # 碰撞后，将player 垂直方向的速度归0(否则物体还是会继续向下掉)
            self.player.vel.y = 0

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

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
