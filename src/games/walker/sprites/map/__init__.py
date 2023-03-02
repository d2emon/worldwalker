"""Main map sprite.

Typical usage example:

  map_sprite = MapSprite(rect)
"""

import pygame
import config
from .image import MapImage
from ...screens.items import load_items
from ..background.image import BackgroundImage


class MapSprite(pygame.sprite.Sprite):
    """Main map sprite.

    Attributes:
        image (pygame.Surface): Sprite image.
        rect (pygame.Rect): Sprite rect.
        show_grid (bool): To show grid.
        starting_pos (tuple): Starting viewpoint.
        viewpoint (pygame.Rect): Source rect.
    """

    __filename = config.Universe.GLOBAL_MAP
    __grid_step = 100

    __bg_image = None

    def __init__(
        self,
        rect,
        items=None,
        starting_pos=(500, 500),
        size=(1000, 1000),
    ):
        """Initialize sprite.

        Args:
            rect (pygame.Rect): Sprite rect.
            items (pygame.sprite.Group): Map items.
            starting_pos (tuple, optional): Starting viewpoint. Defaults to (500, 500).
            size (tuple, optional): Starting viewpoint. Defaults to (1000, 1000).
        """
        super().__init__()

        self.image = pygame.Surface((rect.width, rect.height))
        self.rect = pygame.Rect(rect)

        if self.__bg_image is None:
            MapSprite.__bg_image = BackgroundImage((rect.width, rect.height))

        self.__map_image = MapImage.scaled(
            self.__filename,
            items=items,
            size=size,
            step=self.__grid_step,
        )

        self.items = items
        self.show_grid = False
        self.starting_pos = starting_pos
        self.size = size
        self.viewpoint = pygame.Rect(rect)

        self.reset_viewpoint()

    def set_viewpoint(self, viewpoint):
        """Set map viewpoint.

        Args:
            viewpoint (tuple): Coords of viewpoint.
        """
        self.viewpoint.center = viewpoint

    def reset_viewpoint(self, *args, **kwargs):
        """Reset map viewpoint."""
        self.set_viewpoint(self.starting_pos)

    def switch_grid(self, *args, **kwargs):
        """Switch show grid."""
        # self.show_grid = not self.show_grid
        self.__map_image.switch_grid()
        # self.__map_image.update(self.show_grid)

    def update(self, *args, **kwargs):
        """Update map image."""
        self.image.blit(self.__bg_image, self.rect)
        self.image.blit(self.__map_image, self.rect, self.viewpoint)
