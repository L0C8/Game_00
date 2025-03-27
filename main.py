import pygame
from gameworld import GameWorld
from gui import Gui

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Game_00")
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

world = GameWorld(640, 480, 16, font, view_size=(384, 384), view_offset=(32, 32))
gui = Gui(font, screen.get_width(), screen.get_height())
gui.world_ref = world

running = True
while running:
    for event in pygame.event.get():
        gui.handle_event(event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            world.handle_input(event.key)

    screen.fill((0, 0, 0))
    world.render(screen)
    gui.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()