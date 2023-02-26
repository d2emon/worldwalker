"""Coord label.

Typical usage example:

  label = CoordLabel()
"""

import pygame


class CoordLabel(pygame.sprite.Sprite):
    """Coord label.

    Attributes:
        image (pygame.Surface): Sprite image.
        rect (pygame.Rect): Sprite rect.
        font (pygame.Font): Label font.
    """

    def __init__(self):
        """Initialize label."""
        super().__init__()

        self.font = pygame.font.SysFont('Sans', 16)
        self.x = self.y = 0

    def update(self, *args, **kwargs):
        """Update label."""
        label = f"{self.x} {self.y}"
        image = self.font.render(label, None, (0, 0, 0))

        self.image = image
        self.rect = image.get_rect()
