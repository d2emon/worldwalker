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
        color (pygame.Color): Label color.
        font (pygame.Font): Label font.
        pos (list): Player coords.
    """

    def __init__(self, rect):
        """Initialize label.
        
        Args:
            rect (pygame.Rect): Label rect.
        """
        super().__init__()

        self.color = (255, 255, 255)
        self.font = pygame.font.SysFont('Sans', 16)
        self.pos = [0, 0]

        self.image = pygame.Surface((0, 0))
        self.rect = rect

    @property
    def label(self):
        """Get label text.

        Returns:
            string: Label text.
        """
        return f"{self.pos[0]} {self.pos[1]}"

    def update(self, *args, **kwargs):
        """Update label."""
        self.image = self.font.render(self.label, None, self.color)
