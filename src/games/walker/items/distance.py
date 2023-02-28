"""Distance sprite."""

import pygame
from .item import Item


class Distance(Item):
    """Distance sprite."""

    color = (0, 255, 0)
    radius = 127
    name = ''

    @property
    def size(self):
        """Get item diameter.

        Returns:
            int: Item diameter.
        """
        return int(self.radius * 2)

    def draw(self, rect):
        """Draw item.

        Args:
            rect (pyugame.Rect): Image rect.
        """
        pygame.draw.circle(self.image, self.color, rect.center, self.radius, 1)

        self.draw_label(self.name, rect.center)
