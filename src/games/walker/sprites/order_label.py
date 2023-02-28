"""Order label.

Typical usage example:

  label = OrderLabel()
"""

import pygame


class OrderLabel(pygame.sprite.Sprite):
    """Order label.

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
        self.value = 24

        self.image = pygame.Surface((0, 0))
        self.rect = rect

    def update(self, *args, **kwargs):
        """Update label."""
        self.image = self.font.render(str(self.value), None, self.color)
