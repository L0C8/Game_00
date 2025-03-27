# gameworld.py
import pygame
import random

# Color palette
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
OLIVE   = (128, 128, 0)
NAVY    = (0, 0, 128)
TEAL    = (0, 128, 128)
SILVER  = (192, 192, 192)

class GameWorld:
    def __init__(self, width, height, tile_size, font, view_size=(256, 256), view_offset=(0, 0)):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.font = font
        self.view_width, self.view_height = view_size
        self.view_offset_x, self.view_offset_y = view_offset

        self.view_cols = self.view_width // tile_size
        self.view_rows = self.view_height // tile_size
        self.world_cols = 100
        self.world_rows = 100

        self.grid = [[" " for _ in range(self.world_cols)] for _ in range(self.world_rows)]

        # Place 5 rocks
        rock_positions = set()
        while len(rock_positions) < 5:
            rx = random.randint(0, self.world_cols - 1)
            ry = random.randint(0, self.world_rows - 1)
            if (rx, ry) not in rock_positions:
                rock_positions.add((rx, ry))
                self.grid[ry][rx] = "#"

        # Place player
        while True:
            self.player_x = random.randint(0, self.world_cols - 1)
            self.player_y = random.randint(0, self.world_rows - 1)
            if self.grid[self.player_y][self.player_x] == " ":
                self.grid[self.player_y][self.player_x] = "@"
                break

    def handle_input(self, key):
        dx, dy = 0, 0
        if key == pygame.K_LEFT:
            dx = -1
        elif key == pygame.K_RIGHT:
            dx = 1
        elif key == pygame.K_UP:
            dy = -1
        elif key == pygame.K_DOWN:
            dy = 1

        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if 0 <= new_x < self.world_cols and 0 <= new_y < self.world_rows:
            if self.grid[new_y][new_x] == " ":
                self.grid[self.player_y][self.player_x] = " "
                self.player_x, self.player_y = new_x, new_y
                self.grid[self.player_y][self.player_x] = "@"

    def render(self, surface):
        cam_x = max(0, min(self.player_x - self.view_cols // 2, self.world_cols - self.view_cols))
        cam_y = max(0, min(self.player_y - self.view_rows // 2, self.world_rows - self.view_rows))

        for y in range(self.view_rows):
            for x in range(self.view_cols):
                world_x = cam_x + x
                world_y = cam_y + y
                char = self.grid[world_y][world_x]
                if char == "@":
                    color = CYAN
                elif char == "#":
                    color = GRAY
                else:
                    continue
                text = self.font.render(char, True, color)
                screen_x = self.view_offset_x + x * self.tile_size
                screen_y = self.view_offset_y + y * self.tile_size
                surface.blit(text, (screen_x, screen_y))

        # Draw outline
        outline_rect = pygame.Rect(
            self.view_offset_x - 1, 
            self.view_offset_y - 1, 
            self.view_width + 2, 
            self.view_height + 2
        )
        pygame.draw.rect(surface, WHITE, outline_rect, 1)