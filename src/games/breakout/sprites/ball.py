import random
import pygame
from windows.controls.moving import Moving


class Ball(Moving):
    def __init__(
        self,
        pos=None,
        speed=(0, 1),
    ):
        super().__init__(pygame.Rect(0, 0, 10, 10), speed)
        self.image = self.draw()
        self.rect.center = pos or self.rect.center

    @classmethod
    def draw(cls):
        color = (0, 255, 0)
        r = 5

        image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(image, color, image.get_rect().center, r)
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
