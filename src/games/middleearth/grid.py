from pygame import Surface, Color, Rect, RLEACCEL
from pygame.sprite import DirtySprite
import pygame.draw


TRANSPARENT = Color(255, 0, 255)
GRID_COLOR = Color(128, 128, 128)


class MapGrid(DirtySprite):
    def __init__(self, width, height, grid_size):
        self._layer = 2
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(TRANSPARENT)
        self.rect = self.image.get_rect()

        self.visible = False

        x_size = int(self.image.get_width() / grid_size)
        y_size = int(self.image.get_height() / grid_size)

        for i in range(x_size):
            for j in range(y_size):
                rect = Rect(i * grid_size, j * grid_size, grid_size, grid_size)
                pygame.draw.rect(self.image, GRID_COLOR, rect, 1)
        self.image.set_colorkey(TRANSPARENT, RLEACCEL)

    def toggle(self):
        self.visible = not self.visible
        self.dirty = True
