import pygame
from .sprite import BreakoutSprite


class Brick(BreakoutSprite):
    def __init__(
        self,
        rect=None,
        color=None,
        effect=None,
    ):
        self.color = color or (0, 0, 255)
        super().__init__(rect or pygame.Rect(0, 0, 80, 20))
        self.effect = effect
        self.points = 10

    def draw(self):
        image = pygame.Surface((self.rect.width, self.rect.height))
        image.fill(self.color)
        return image
