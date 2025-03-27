# gameworld.py
import pygame
import random
from game.objs import Object, Actor

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

        self.grid = [[None for _ in range(self.world_cols)] for _ in range(self.world_rows)]
        self.actors = []
        self.turn_queue = []
        self.current_actor_index = 0
        self.current_actor_moves = 0

        # Place Player
        while True:
            x = random.randint(0, self.world_cols - 1)
            y = random.randint(0, self.world_rows - 1)
            if self.grid[y][x] is None:
                player = Actor(x, y, "@", "Player", CYAN, 0, hp=20, att=3, str=2, int=2, dex=2, end=2, spd=3)
                self.grid[y][x] = player
                self.actors.append(player)
                self.player = player
                break

        # Place Rocks
        rock_count = 55
        while rock_count > 0:
            x = random.randint(0, self.world_cols - 1)
            y = random.randint(0, self.world_rows - 1)
            if self.grid[y][x] is None:
                self.grid[y][x] = Object(x, y, "#", "Rock", GRAY, 1)
                rock_count -= 1

        # Place Enemies
        enemy_count = 25
        while enemy_count > 0:
            x = random.randint(0, self.world_cols - 1)
            y = random.randint(0, self.world_rows - 1)
            if self.grid[y][x] is None:
                enemy = Actor(x, y, "&", "Enemy", RED, 2, hp=10, att=2, str=1, int=1, dex=1, end=1, spd=2)
                self.grid[y][x] = enemy
                self.actors.append(enemy)
                enemy_count -= 1

        self.handle_turns()  # <-- Initialize the turn queue at the end of setup

    def handle_turns(self):
        queue = sorted(self.actors, key=lambda a: (-a.spd, random.random()))
        self.turn_queue = queue.copy()
        self.current_actor_index = 0
        self.current_actor_moves = 0

    def ai_move(self, actor):
        dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
        new_x = actor.x + dx
        new_y = actor.y + dy
        if 0 <= new_x < self.world_cols and 0 <= new_y < self.world_rows:
            if self.grid[new_y][new_x] is None:
                self.grid[actor.y][actor.x] = None
                actor.move(dx, dy)
                self.grid[actor.y][actor.x] = actor

    def move_player(self, dx, dy):
        if not self.turn_queue:
            return  # Defensive guard

        actor = self.turn_queue[self.current_actor_index]
        if actor != self.player or self.current_actor_moves >= actor.end:
            return

        new_x = actor.x + dx
        new_y = actor.y + dy
        if 0 <= new_x < self.world_cols and 0 <= new_y < self.world_rows:
            if self.grid[new_y][new_x] is None:
                self.grid[actor.y][actor.x] = None
                actor.move(dx, dy)
                self.grid[actor.y][actor.x] = actor
                self.current_actor_moves += 1

        if self.current_actor_moves >= actor.end:
            self.current_actor_index += 1
            self.process_turn_queue()
            self.handle_turns()

    def process_turn_queue(self):
        while self.current_actor_index < len(self.turn_queue):
            actor = self.turn_queue[self.current_actor_index]
            self.current_actor_moves = 0
            if actor == self.player:
                return  # wait for player input
            for _ in range(actor.end):
                self.ai_move(actor)
            self.current_actor_index += 1

    def handle_input(self, key):
        dx, dy = 0, 0
        if key == pygame.K_LEFT: dx = -1
        elif key == pygame.K_RIGHT: dx = 1
        elif key == pygame.K_UP: dy = -1
        elif key == pygame.K_DOWN: dy = 1
        if dx != 0 or dy != 0:
            self.move_player(dx, dy)

    def render(self, surface):
        cam_x = max(0, min(self.player.x - self.view_cols // 2, self.world_cols - self.view_cols))
        cam_y = max(0, min(self.player.y - self.view_rows // 2, self.world_rows - self.view_rows))

        mouse_name = ""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for y in range(self.view_rows):
            for x in range(self.view_cols):
                wx = cam_x + x
                wy = cam_y + y
                if wx >= self.world_cols or wy >= self.world_rows:
                    continue
                obj = self.grid[wy][wx]
                screen_x = self.view_offset_x + x * self.tile_size
                screen_y = self.view_offset_y + y * self.tile_size
                if (0 <= screen_x < self.width) and (0 <= screen_y < self.height):
                    if obj:
                        obj.render(surface, self.font, self.tile_size, screen_x, screen_y)
                        if screen_x <= mouse_x < screen_x + self.tile_size and screen_y <= mouse_y < screen_y + self.tile_size:
                            mouse_name = obj.name

        outline_rect = pygame.Rect(
            self.view_offset_x - 1,
            self.view_offset_y - 1,
            self.view_width + 2,
            self.view_height + 2
        )
        pygame.draw.rect(surface, WHITE, outline_rect, 1)

        if mouse_name:
            label = self.font.render(mouse_name, True, WHITE)
            surface.blit(label, (4, 4))