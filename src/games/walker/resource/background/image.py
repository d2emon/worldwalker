"""Main background image.

Typical usage example:

  background = Background((1000, 1000))
"""

import pygame


class BackgroundImage(pygame.Surface):
    """Background image."""

    def __init__(self, size):
        """Initialize sprite.

        Args:
            size (tuple): Image size.
        """
        super().__init__(size)

        self.color = (0, 0, 0)
        self.draw()

    def draw(self):
        """Draw sprite."""
        self.fill(self.color)

