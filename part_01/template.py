import pygame
from part_01.settings import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

# Game loop
running = True
while running:

    # keep loop running at the right speed
    clock.tick(FPS)

    # process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # update
    all_sprites.update()

    # draw /render
    screen.fill(BLACK)
    all_sprites.draw()

    # flip/update the screen
    pygame.display.update()

pygame.quit()
