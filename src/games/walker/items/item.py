"""Item sprite."""

import pygame


class Item(pygame.sprite.Sprite):
    """Item sprite."""

    base_scale = 0
    base_size = 100

    label_color = (255, 255, 255)
    label_font = 'Sans'
    label_size = 16

    name = ''

    def __init__(self, position=(500, 500), scale=1.0):
        """Initialize sprite.

        Args
            position (tuple, optional): Starting position. Defaults to (500, 500).
        """
        super().__init__()

        self.scale = scale
        self.image = pygame.Surface((self.size, self.size), flags=pygame.SRCALPHA)

        rect = self.image.get_rect()
        self.rect = pygame.Rect(rect)
        self.rect.center = position

        self.draw(rect)
        print(self.name, self.size)

    @property
    def size_modifier(self):
        """Get item diameter.

        Returns:
            int: Item diameter.
        """
        order = self.base_scale - self.scale

        if order < 0:
            return 1

        if order > 2:
            return 0

        return 10 ** order

    @property
    def size(self):
        """Get item diameter.

        Returns:
            int: Item diameter.
        """
        return int(self.base_size * self.size_modifier)

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
