"""Main map sprite.

Typical usage example:

  map_sprite = MapSprite(rect)
"""

import pygame


def background(image):
    """Draw background for map.

    Args:
        image (pygame.Surface): Image to fill.
    """
    image.fill((0, 0, 0))


class MapSprite(pygame.sprite.Sprite):
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

        self.__map_image = image

        self.image = pygame.Surface((rect.width, rect.height))
        self.rect = pygame.Rect(rect)

        self.__step = step
        self.starting_pos = viewpoint
        self.viewpoint = pygame.Rect(rect)

        self.reset_viewpoint()

    def reset_viewpoint(self, *args, **kwargs):
        self.viewpoint.center = self.starting_pos

    def switch_grid(self, *args, **kwargs):
        self.__map_image.show_grid = not self.__map_image.show_grid
        self.__map_image.update()

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
