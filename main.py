import pygame
import random
import os

pygame.init()

# Window settings
WIDTH, HEIGHT = 640, 480
TILE_SIZE = 16
VIEW_COLS = WIDTH // TILE_SIZE
VIEW_ROWS = HEIGHT // TILE_SIZE

# World settings
WORLD_COLS = 100
WORLD_ROWS = 100

# Colors
BLACK   = (0, 0, 0)
GRAY    = (100, 100, 100)
WHITE   = (255, 255, 255)
CYAN    = (0, 255, 255)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
YELLOW  = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE  = (255, 165, 0)
PINK    = (255, 105, 180)
PURPLE  = (128, 0, 128)
BROWN   = (139, 69, 19)
NAVY    = (0, 0, 128)


# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rogue")

# Font setup
FONT_PATH = os.path.join(os.path.dirname(__file__), "ndsbios_memesbruh03.ttf")
font = pygame.font.Font(FONT_PATH, TILE_SIZE)

# Initialize world grid
grid = [[" " for _ in range(WORLD_COLS)] for _ in range(WORLD_ROWS)]

# Place rocks randomly
rock_positions = set()
while len(rock_positions) < 250:
    rx = random.randint(0, WORLD_COLS - 1)
    ry = random.randint(0, WORLD_ROWS - 1)
    if (rx, ry) not in rock_positions:
        rock_positions.add((rx, ry))
        grid[ry][rx] = "#"

while True:
    player_x = random.randint(0, WORLD_COLS - 1)
    player_y = random.randint(0, WORLD_ROWS - 1)
    if grid[player_y][player_x] == " ":
        grid[player_y][player_x] = "@"
        break

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Camera view top-left corner
    cam_x = max(0, min(player_x - VIEW_COLS // 2, WORLD_COLS - VIEW_COLS))
    cam_y = max(0, min(player_y - VIEW_ROWS // 2, WORLD_ROWS - VIEW_ROWS))

    for y in range(VIEW_ROWS):
        for x in range(VIEW_COLS):
            world_x = cam_x + x
            world_y = cam_y + y
            char = grid[world_y][world_x]
            if char == "@":
                color = CYAN
            elif char == "#":
                color = GRAY
            else:
                continue
            text = font.render(char, True, color)
            screen.blit(text, (x * TILE_SIZE, y * TILE_SIZE))

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            dx, dy = 0, 0
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_UP:
                dy = -1
            elif event.key == pygame.K_DOWN:
                dy = 1

            new_x = player_x + dx
            new_y = player_y + dy

            if 0 <= new_x < WORLD_COLS and 0 <= new_y < WORLD_ROWS:
                if grid[new_y][new_x] == " ":
                    grid[player_y][player_x] = " "
                    player_x, player_y = new_x, new_y
                    grid[player_y][player_x] = "@"

pygame.quit()
