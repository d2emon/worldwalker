"""Player sprite.

Typical usage example:

  player = Player((0, 0))
"""

import pygame
from pygame.sprite import Sprite


__PLAYER_SIZE = 10
__PLAYER_VIEW = 5
__PLAYER_COLOR = (255, 255, 0)
__PLAYER_VIEW_COLOR = (0, 0, 255)


def __draw_player(image, size, color):
    """Draw player image.

    Args:
        image (pygame.Image): Sprite image.
        size (float): Player size.
        color (pygame.Color): Player color.
    """
    rect = image.get_rect()
    pygame.draw.circle(image, color, rect.center, size)


def __draw_view(image, size, color):
    """Draw player image.

    Args:
        image (pygame.Image): Sprite image.
        size (float): View area size.
        color (pygame.Color): View area color.
    """
    rect = image.get_rect()
    pygame.draw.circle(image, color, rect.center, size, 2)


def draw(scale=1.0):
    """Draw player image.

    Args:
        scale (float): Map scale.
    Returns:
        pygame.Surface: Loaded image.
    """
    radius = __PLAYER_VIEW * scale
    width = height = radius * 2
    image = pygame.Surface((width, height), flags=pygame.SRCALPHA)
    __draw_player(image, __PLAYER_SIZE, __PLAYER_COLOR)
    __draw_view(image, radius, __PLAYER_VIEW_COLOR)
    return image


class Player(Sprite):
    """Player sprite.

    Attributes:
        image (pygame.Surface): Sprite image.
        rect (pygame.Rect): Sprite rect.
        speed (float): Rect speed.
    """

    __SPEED = 10

    def __init__(self, center=(0, 0), scale=1.0):
        """Initialize sprite.

        Args:
            center (tuple): Sprite center.
            scale (float): Image scale.
        """
        super().__init__()
        self.image = draw(scale)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = self.__SPEED
