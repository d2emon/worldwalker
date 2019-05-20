from pygame import Surface, Color, Rect, RLEACCEL
import pygame.draw


TRANSPARENT = Color(255, 0, 255)
GRID_COLOR = Color(128, 128, 128)


class MapGrid(Surface):
    def __init__(self, width, height, grid_size):
        Surface.__init__(self, (width, height))
        self.fill(TRANSPARENT)
        xsize = int(self.get_width() / grid_size)
        ysize = int(self.get_height() / grid_size)
        for i in range(xsize):
            for j in range(ysize):
                rect = Rect(i * grid_size, j * grid_size, grid_size, grid_size)
                pygame.draw.rect(self, GRID_COLOR, rect, 1)
        self.set_colorkey(TRANSPARENT, RLEACCEL)

    def draw(self, screen):
        screen.blit(self, (0, 0))
