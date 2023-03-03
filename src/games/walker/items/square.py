"""Square item."""

import pygame
from .item import Item, ItemFactory


class SquareSprite(Item):
    def draw(self, rect):
        """Draw item.

        Args:
            rect (pygame.Rect): Image rect.
        """
        pygame.draw.rect(self.image, self.color, rect, self.border)

        self.draw_label(self.name, rect.center)


class Square(ItemFactory):
    """Square sprite."""
    color = (128, 128, 128)
    border = 0
    model = SquareSprite
