"""Circular sprite."""

import pygame
from .item import Item


class Circular(Item):
    """Circular sprite."""

    color = (128, 128, 128)
    size = 100
    name = ''

    def draw(self, rect):
        """Draw item.

        Args:
            rect (pyugame.Rect): Image rect.
        """
        pygame.draw.circle(self.image, self.color, rect.center, self.size / 2)

        self.draw_label(self.name, rect.center)
