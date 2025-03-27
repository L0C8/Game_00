class Object:
    def __init__(self, x, y, char, name, color, index):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.index = index

    def render(self, surface, font, tile_size, offset_x=0, offset_y=0):
        text = font.render(self.char, True, self.color)
        surface.blit(text, (offset_x + self.x * tile_size, offset_y + self.y * tile_size))

class Actor(Object):
    def __init__(self, x, y, char, name, color, index, hp=10, attack=1):
        super().__init__(x, y, char, name, color, index)
        self.hp = hp
        self.attack = attack

    def move(self, dx, dy):
        self.x += dx
        self.y += dy