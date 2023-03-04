"""Item sprite."""

import pygame


class Item(pygame.sprite.Sprite):
    """Item sprite."""

    label_color = (255, 255, 255)
    label_font = 'Sans'
    label_size = 16

    def __init__(
        self,
        name='',
        position=(500, 500),
        size=(100, 100),
        color=(0, 0, 0),
        border=0,
        visible=True,
    ):
        """Initialize sprite.

        Args
            position (tuple, optional): Starting position. Defaults to (500, 500).
            size (tuple, optional): Item size. Defaults to (100, 100).
        """
        super().__init__()

        self.name = name
        self.size = size
        self.color = color
        self.border = border
        self.visible = visible

        self.image = pygame.Surface(size, flags=pygame.SRCALPHA)

        rect = self.image.get_rect()
        self.rect = pygame.Rect(rect)
        self.rect.center = position

        self.draw(rect)

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


class ItemFactory:
    """Item sprite factory."""

    model = Item
    default_name = ''
    base_scale = 0
    base_size = 1.0
    color = (0, 0, 0)
    border = 0

    def __init__(
        self,
        name=None,
        scale=None,
        size=None,
        color=None,
        border=None,
        visible=True,
    ):
        self.name = name or self.default_name
        self.item_size = size or self.base_size
        self.scale = scale or self.base_scale
        self.item_color = color or self.color
        self.item_border = border or self.border
        self.visible = visible

    def get_size_modifier(self, scale=1.0):
        """Get item size modifier.

        Returns:
            int: Item size modifier.
        """
        order = self.scale - scale

        if order < 0:
            return 0

        if order > 2:
            return 0

        return 10 ** order

    def get_size(self, size=None, scale=1.0):
        """Get item size.

        Returns:
            int: Item size.
        """
        if size is None:
            size = (self.item_size, self.item_size)

        modifier = self.get_size_modifier(scale)
        return [int(item * modifier) for item in size]

    def __call__(self, position=(500, 500), scale=1.0, size=None):
        item_size = self.get_size(size, scale)
        return self.model(
            name=self.name,
            position=position,
            size=item_size,
            color=self.item_color,
            border=self.item_border,
            visible=self.visible,
        )
