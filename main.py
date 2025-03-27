# main.py
import pygame
from gameworld import GameWorld

pygame.init()

WIDTH, HEIGHT = 640, 480
TILE_SIZE = 16
FONT_PATH = "assets/ndsbios_memesbruh03.ttf"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rogue")
font = pygame.font.Font(FONT_PATH, TILE_SIZE)

world = GameWorld(
    width=WIDTH,
    height=HEIGHT,
    tile_size=TILE_SIZE,
    font=font,
    view_size=(256, 256),
    view_offset=(64, 64)
)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))
    world.render(screen)
    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            world.handle_input(event.key)

pygame.quit()
