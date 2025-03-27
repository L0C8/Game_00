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
        surface.blit(text, (offset_x, offset_y))

class Actor(Object):
    def __init__(self, x, y, char, name, color, index, hp=10, att=1, str=1, int=1, dex=1, end=1, spd=1):
        super().__init__(x, y, char, name, color, index)
        self.hp = hp
        self.att = att
        self.str = str 
        self.int = int
        self.dex = dex
        self.end = end
        self.spd = spd


    def move(self, dx, dy):
        self.x += dx
        self.y += dy