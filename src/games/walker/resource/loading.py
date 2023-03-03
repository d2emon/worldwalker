"""Loading label.

Typical usage example:

  label = Loading()
"""

import pygame


class LoadingLabel(pygame.sprite.Sprite):
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
        self.font = pygame.font.SysFont('Sans', 128)
        self.field = rect

        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(rect)

        self.update()


    def update(self, *args, **kwargs):
        """Update label."""
        self.image = self.font.render("Loading...", None, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.field.center
