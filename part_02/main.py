from part_02.sprites import *
from part_02.sprites import Player


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
        # 创建玩家实例，并加入容器
        self.player = Player()
        self.all_sprites.add(self.player)
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
        pg.display.update()

    # 为了方便观察pos,vel,acc这些变量，定义一个debug辅助函数
    def debug(self):
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
