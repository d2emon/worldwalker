"""Order label.

Typical usage example:

  label = OrderLabel()
"""

import pygame


class MapLabel(pygame.sprite.Sprite):
    """Order label.

    Attributes:
        image (pygame.Surface): Sprite image.
        rect (pygame.Rect): Sprite rect.
        color (pygame.Color): Label color.
        font (pygame.Font): Label font.
        pos (list): Player coords.
    """

    def __init__(self, caption, rect, font_size=32):
        """Initialize label.
        
        Args:
            caption (string): Item caption.
            rect (pygame.Rect): Label rect.
        """
        super().__init__()

        self.color = (255, 255, 255)
        self.font = pygame.font.SysFont('Sans', font_size)
        self.caption = caption

        self.name = f"Label: '{caption}'"
        self.visible = True

        self.image = pygame.Surface((0, 0))
        self.rect = pygame.Rect(rect)

    def update(self, *args, **kwargs):
        """Update label."""
        self.image = self.font.render(str(self.caption), None, self.color)
