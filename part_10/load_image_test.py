import pygame
from os import path
from xml.dom.minidom import parse

# 游戏中的一些常量定义
SIZE = (WIDTH, HEIGHT) = (400, 400)
FPS = 10

# 颜色常量定义
BLACK = 0, 0, 0
WHITE = 255, 255, 255

# 初始化
pygame.init()
pygame.mixer.init()

# 窗口、标题等初始化
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

spritesheet_image_file_name = path.join(path.dirname(__file__), "../img/spritesheet_jumper.png")
spritesheet_xml_file_name = path.join(path.dirname(__file__), "../img/spritesheet_jumper.xml")
spritesheet_image = pygame.image.load(spritesheet_image_file_name)
spritesheet_image.set_colorkey(BLACK)
spritesheet_dom_tree = parse(spritesheet_xml_file_name)
root_textures = spritesheet_dom_tree.documentElement
sub_textures = root_textures.getElementsByTagName("SubTexture")
dic_image = {}


def get_image_rect(img_name):
    if dic_image.get(img_name):
        return dic_image[img_name]
    for texture in sub_textures:
        name = texture.getAttribute("name")
        if img_name == name:
            dic_image[img_name] = pygame.Rect(
                int(texture.getAttribute("x")),
                int(texture.getAttribute("y")),
                int(texture.getAttribute("width")),
                int(texture.getAttribute("height"))
            )
            return dic_image[img_name]


def get_image(img_name, angle=0, scale=1.0):
    rect = get_image_rect(img_name);
    image = pygame.Surface((rect.width, rect.height))
    image.blit(spritesheet_image, (0, 0), rect)
    image.set_colorkey(BLACK)
    new_image = pygame.transform.rotozoom(image, angle, scale)
    new_image.set_colorkey(BLACK)
    return new_image


# 循环入口
running = True
while running:

    # 设置帧数
    clock.tick(FPS)

    # 事件处理
    for event in pygame.event.get():
        # 退出处理
        if event.type == pygame.QUIT:
            running = False

    # (update) 游戏更新逻辑(比如：改动角色的位置或一些重要变量等，这里仅演示更新当前时间)
    image1 = get_image("bunny1_hurt.png", 0, 0.5)
    image2 = get_image("bunny1_walk1.png", 45, 0.5)
    image3 = get_image("bunny2_stand.png", -45, 0.5)

    # (draw)渲染屏幕
    screen.fill(BLACK)  # 先准备一块黑布
    screen.blit(image1, (0, 0), image1.get_rect())
    screen.blit(image2, (200, 200), image2.get_rect())
    screen.blit(image3, (200, 50), image3.get_rect())

    # 屏幕内容刷新
    pygame.display.update()

# 循环结束后，退出游戏
pygame.quit()
