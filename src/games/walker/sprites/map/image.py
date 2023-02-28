"""Main map image.

Typical usage example:

  map_image = MapImage(image)
"""

import pygame
from .grid import Grid


MAP_SCALE = 0.5


class MapImage(pygame.Surface):
    """Main map sprite.

    Attributes:
        grid (Grid): Grid for image.
    """

    def __init__(self, image, items=None, step=None):
        """Initialize sprite.

        Args:
            image (pygame.Image): Base image.
            items (pygame.sprite.Group, optional): Map items. Defaults to None.
            step (float): Step for grid.
        """
        super().__init__((1000, 1000))

        self.image = image

        self.items = items

        self.show_grid = False
        self.grid = Grid(
            size=(1000, 1000),
            step=step,
        )

        self.update()

    def update(self, show_grid=False):
        """Update map image.
        
        Args:
            show_grid (bool): To show grid.
        """
        self.items.update()

        self.blit(self.image, self.get_rect())

        if self.items:
            self.items.draw(self)

        if show_grid:
            self.grid.draw(self)

    @classmethod
    def scaled(cls, filename, items, scale=None, step=None):
        """Draw map image.

        Args:
            filename (string): Filename with image.
            items (list): Map items.
            scale (float): Scale for image.
            step (float): Step for grid.
        Returns:
            pygame.Surface: Loaded image.
        """
        image = pygame.image.load(filename)

        if scale:
            image = pygame.transform.scale(
                image,
                (
                    int(image.get_width() * MAP_SCALE),
                    int(image.get_height() * MAP_SCALE),
                ),
            )

        return cls(image, items, step=step)
