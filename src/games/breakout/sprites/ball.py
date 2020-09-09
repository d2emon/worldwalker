import random
import pygame
from pygame import draw, Rect
from .sprite import BreakoutSprite


class Ball(BreakoutSprite):
    def __init__(
        self,
        rect=None,
        pos=None,
        color=None,
        radius=5,
        speed=None,
    ):
        self.r = radius
        self.color = color or (0, 255, 0)
        super().__init__(
            rect or pygame.Rect(0, 0, 10, 10),
            pos,
            speed or (random.randint(-2, 2), 1),
        )

    def draw(self):
        image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        rect = image.get_rect()
        pygame.draw.circle(image, self.color, rect.center, self.r)
        pygame.draw.circle(image, (255, 0, 0), (2, 2), 2)
        return image

    def reverse_x(self):
        x, y = self.speed
        self.speed = -x, y

    def reverse_y(self):
        x, y = self.speed
        self.speed = x, -y

    def struck(self, speed):
        x, y = self.speed
        dx, dy = speed
        self.speed = (x + dx), -(y + dy)
