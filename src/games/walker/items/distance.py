"""Distance sprite."""

import pygame
from .item import Item, ItemFactory


class DistanceSprite(Item):
    def draw(self, rect):
        """Draw item.

        Args:
            rect (pyugame.Rect): Image rect.
        """
        pygame.draw.circle(self.image, self.color, rect.center, self.size[0] / 2, 1)

        self.draw_label(self.name, rect.center)


class Distance(ItemFactory):
    """Distance sprite."""
    color = (0, 255, 0)
    radius = 127
    model = DistanceSprite

    def __init__(self, name=None, scale=None, size=None, color=None, border=None):
        diameter = (size if size is not None else self.radius) * 2
        super().__init__(
            name=name,
            scale=scale,
            size=diameter,
            color=color,
            border=border,
        )
