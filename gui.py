# gui.py
import pygame

class Gui:
    def __init__(self, font, screen_width, screen_height):
        self.font = font
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.buttons = []
        self.messages = []
        self.world_ref = None
        self.message_box_height = 80
        self._setup_buttons()

    def _setup_buttons(self):
        self.buttons.append({
            'label': 'Inspect',
            'rect': pygame.Rect(self.screen_width - 110, 10, 100, 30),
            'callback': self.on_inspect
        })
        self.inspecting = False

    def draw(self, surface):
        # Draw buttons
        for btn in self.buttons:
            pygame.draw.rect(surface, (200, 200, 200), btn['rect'])
            text = self.font.render(btn['label'], True, (0, 0, 0))
            surface.blit(text, (btn['rect'].x + 10, btn['rect'].y + 5))

        # Draw message box
        box_y = self.screen_height - self.message_box_height
        pygame.draw.rect(surface, (30, 30, 30), (0, box_y, self.screen_width, self.message_box_height))
        for i, msg in enumerate(self.messages[-3:]):  # Show last 3 messages
            text = self.font.render(msg, True, (255, 255, 255))
            surface.blit(text, (10, box_y + 5 + i * 20))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in self.buttons:
                if btn['rect'].collidepoint(event.pos):
                    btn['callback']()
                    return
            if self.inspecting:
                self.inspect_click(event.pos)
                self.inspecting = False

    def on_inspect(self):
        self.inspecting = True
        self.add_message("Inspect button clicked!")

    def inspect_click(self, pos):
        if self.world_ref is None:
            return
        tile_x = (pos[0] - self.world_ref.view_offset_x) // self.world_ref.tile_size
        tile_y = (pos[1] - self.world_ref.view_offset_y) // self.world_ref.tile_size

        cam_x = max(0, min(self.world_ref.player.x - self.world_ref.view_cols // 2, self.world_ref.world_cols - self.world_ref.view_cols))
        cam_y = max(0, min(self.world_ref.player.y - self.world_ref.view_rows // 2, self.world_ref.world_rows - self.world_ref.view_rows))

        world_x = cam_x + tile_x
        world_y = cam_y + tile_y

        if 0 <= world_x < self.world_ref.world_cols and 0 <= world_y < self.world_ref.world_rows:
            obj = self.world_ref.grid[world_y][world_x]
            if obj:
                self.add_message(f"Inspected: {obj.name}")
            else:
                self.add_message("Nothing here.")

    def add_message(self, msg):
        self.messages.append(msg)
        if len(self.messages) > 50:
            self.messages = self.messages[-50:]
