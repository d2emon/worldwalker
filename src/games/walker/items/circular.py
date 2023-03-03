"""Circular sprite."""

import pygame
from .item import Item, ItemFactory


class CircularSprite(Item):
    def draw(self, rect):
        """Draw item.

        Args:
            rect (pygame.Rect): Image rect.
        """
        pygame.draw.circle(self.image, self.color, rect.center, self.size[0] / 2, self.border)

        self.draw_label(self.name, rect.center)


class Circular(ItemFactory):
    """Circular sprite."""
    color = (128, 128, 128)
    border = 0
    model = CircularSprite
