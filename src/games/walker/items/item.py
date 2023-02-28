"""Item sprite."""

import pygame


class Item(pygame.sprite.Sprite):
    """Item sprite."""

    size = 100

    label_color = (255, 255, 255)
    label_font = 'Sans'
    label_size = 16

    def __init__(self, position=(500, 500)):
        """Initialize sprite.

        Args
            position (tuple, optional): Starting position. Defaults to (500, 500).
        """
        super().__init__()

        self.image = pygame.Surface((self.size, self.size), flags=pygame.SRCALPHA)

        rect = self.image.get_rect()
        self.draw(rect)

        self.rect = pygame.Rect(rect)
        self.rect.center = position

    def draw(self, rect):
        """Draw item.

        Args:
            rect (pyugame.Rect): Image rect.
        """
        raise NotImplementedError()

    def draw_label(self, text, position=(0, 0)):
        """Draw text label.

        Args:
            text (string): Label text.
            position (tuple, optional): Label position. Defaults to (0, 0).
        """
        font = pygame.font.SysFont(self.label_font, self.label_size)
        label = font.render(text, None, self.label_color)

        rect = label.get_rect()
        rect.center = position

        self.image.blit(label, rect)
