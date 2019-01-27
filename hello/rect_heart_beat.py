import pygame
import math
from hello.settings import *

pygame.init()
win = pygame.display.set_mode(SIZE, 0)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

running = True

image = pygame.Surface((RECT_WIDTH, RECT_WIDTH))
image.fill(GREEN)
angle = 0

while running:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill(BLACK)
    pygame.draw.line(image, RED, (0, 0), (RECT_WIDTH, RECT_WIDTH), 1)
    pygame.draw.line(image, RED, (RECT_WIDTH, 0), (0, RECT_WIDTH), 1)
    new_image = pygame.transform.rotozoom(image, angle, 0.5 + math.fabs(math.sin(angle * 0.15)))
    angle += 1
    win.blit(new_image, new_image.get_rect(center=(WIDTH / 2, HEIGHT / 2)))
    pygame.display.update()

    print(angle)

pygame.quit()
