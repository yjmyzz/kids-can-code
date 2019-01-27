import pygame as pg
from part_01.settings import *


class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.playing = False
        self.all_sprites = []

    # 开始新游戏时的处理(eg: 主角挂了，重新开始；或第1次进入）
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.run()

    # 游戏运行的循环入口
    def run(self):
        # 注：有2个控制变量，running是控制pygame是否退出，而playing是游戏情节是否继续处理
        # (即：有可能游戏情况结束，比如：主角挂了，显示game over，但是pygame并不需要退出）
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # 游戏逻辑更新处理
    def update(self):
        pass

    # 事件处理
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
        pass

    # 屏幕渲染
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.update()

    # 游戏开始的splash图片
    def show_start_screen(self):
        pass

    # game over时的显示
    def show_go_screen(self):
        pass


g = Game()
# 显示开始场景
g.show_start_screen()
while g.running:
    # 开始
    g.new()
    # 主角挂了之后的显示
    g.show_go_screen()

pg.quit()
