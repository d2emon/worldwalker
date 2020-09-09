import pygame
from pygame.sprite import Sprite


class Brick(Sprite):
    def __init__(
        self,
        pos=None,
        effect=None,
    ):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 80, 20)
        self.image = self.draw()
        self.rect.center = pos or self.rect.center

        self.effect = effect
        self.points = 10

    @classmethod
    def draw(cls):
        image = pygame.Surface((80, 20), pygame.SRCALPHA)
        image.fill((0, 0, 255))
        return image
