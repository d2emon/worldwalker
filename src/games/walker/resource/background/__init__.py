"""Main background sprite.

Typical usage example:

  background = Background(rect)
"""

import pygame
from ... import resource
from .image import BackgroundImage


class Background(pygame.sprite.Sprite):
    """Background sprite.

    Attributes:
        image (pygame.Surface): Sprite image.
        rect (pygame.Rect): Sprite rect.
    """

    def __init__(self, rect):
        """Initialize sprite.

        Args:
            rect (pygame.Rect): Sprite rect.
        """
        super().__init__()

        self.rect = pygame.Rect(rect)
        self.image = BackgroundImage(self.rect.size)
        