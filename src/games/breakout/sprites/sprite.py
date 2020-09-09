import pygame
from .moving import Moving


class BreakoutSprite(Moving):
    def __init__(
        self,
        rect,
        pos=None,
        speed=(0, 0),
    ):
        super().__init__(rect, speed)
        if pos:
            self.rect.center = pos
        self.image = self.draw()

    def draw(self):
        return pygame.Surface((self.rect.width, self.rect.height))
