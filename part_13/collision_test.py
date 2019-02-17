import pygame
from os import path
from xml.dom.minidom import parse

SIZE = (WIDTH, HEIGHT) = (265, 320)
FPS = 10

BLACK = 0, 0, 0
WHITE = 255, 255, 255

pygame.init()
pygame.mixer.init()

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


# 解析xml，找出指定图片的坐标、尺寸信息
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


def get_image(img_name):
    rect = get_image_rect(img_name);
    image = pygame.Surface((rect.width, rect.height))
    image.blit(spritesheet_image, (0, 0), rect)
    image.set_colorkey(BLACK)
    return image


class Demo(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


running = True
pos1 = (20, 5)
pos2 = (125, 110)

demo1 = Demo(get_image("bunny1_walk1.png"), pos1)
demo2 = Demo(get_image("bunny2_stand.png"), pos2)

all_sprites = pygame.sprite.Group()
all_sprites.add(demo1)
all_sprites.add(demo2)

group2 = pygame.sprite.Group()
group2.add(demo2)

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    all_sprites.draw(screen)

    pygame.draw.rect(screen, (255, 0, 0), demo1.rect, 1)
    pygame.draw.rect(screen, (0, 255, 0), demo2.rect, 1)

    if pygame.sprite.spritecollideany(demo1, group2, False):
        print("True")
    else:
        print("False")

    pygame.display.update()

pygame.quit()
