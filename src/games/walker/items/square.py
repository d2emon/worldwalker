"""Square item."""

import pygame
from .item import Item


class Square(Item):
    """item sprite."""

    color = (128, 128, 128)
    border = 0

    def draw(self, rect):
        """Draw item.

        Args:
            rect (pyugame.Rect): Image rect.
        """
        pygame.draw.rect(self.image, self.color, rect, self.border)

        self.draw_label(self.name, rect.center)
