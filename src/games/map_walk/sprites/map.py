"""Main map sprite.

Typical usage example:

  map_sprite = MapSprite(rect)
"""

import pygame
from pygame.sprite import Sprite


__MAP_SCALE = 0.5


def background(image):
    """Draw background for map.

    Args:
        image (pygame.Surface): Image to fill.
    """
    image.fill((0, 0, 0))


def __grid(image, step=10, start=(0, 0), size=(100, 100)):
    """Draw grid on image.

    Args:
        image (pygame.Surface): Image to draw grid.
        step (int): Grid step.
        start (tuple): Grid starting position.
        size (tuple): Grid size.
    """
    min_x, min_y = start
    width, height = size
    max_x = image.get_width() - width
    max_y = image.get_height() - height

    # Fill horyzontal lines
    for x in range(min_x, max_x, step):
        pygame.draw.line(image, (0, 0, 0), (x, min_y), (x, max_y))

    # Fill vertical lines
    for y in range(min_y, max_y, step):
        pygame.draw.line(image, (0, 0, 0), (min_x, y), (max_x, y))


def draw_map(filename, scale=1.0, step=None):
    """Draw map image.

    Args:
        filename (string): Filename with image.
        scale (float): Scale for image.
        step (int): Grid step.
    Returns:
        pygame.Surface: Loaded image.
    """
    image = pygame.image.load(filename)

    if scale:
        image = pygame.transform.scale(
            image,
            (
                int(image.get_width() * __MAP_SCALE),
                int(image.get_height() * __MAP_SCALE),
            ),
        )

    if step:
        __grid(
            image,
            size=(200, 300),
            start=(210, 185),
            step=step,
        )

    return image


class MapSprite(Sprite):
    """Main map sprite.

    Attributes:
        image (pygame.Surface): Sprite image.
        rect (pygame.Rect): Sprite rect.
        viewpoint (pygame.Rect): Source rect.
    """

    def __init__(self, image, rect, viewpoint, step):
        """Initialize sprite.

        Args:
            image (pygame.Image): Sprite image.
            rect (pygame.Rect): Sprite rect.
            viewpoint (pygame.Rect): Source rect.
            step (float): Step for movement.
        """
        super().__init__()

        self.__step = step
        self.__map_image = image

        self.image = pygame.Surface((rect.width, rect.height))
        self.rect = pygame.Rect(rect)

        self.viewpoint = pygame.Rect(rect)
        self.viewpoint.center = viewpoint

    def move(self, x, y):
        """Move sprite viewpoint.

        Args:
            x (float): Moves by x.
            y (float): Moves by y.
        """
        self.viewpoint = self.viewpoint.move(x * self.__step, y * self.__step)
        # print(x, y, self.viewpoint.center)

    def update(self, *args, **kwargs):
        """Update map image."""
        background(self.image)
        self.image.blit(self.__map_image, self.rect, self.viewpoint)
