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

    __cached_image = None
    show_grid = True

    def __init__(self, image, items=None, size=(1000, 1000), step=None):
        """Initialize sprite.

        Args:
            image (pygame.Image): Base image.
            items (pygame.sprite.Group, optional): Map items. Defaults to None.
            size (tuple): Map size.
            step (float): Step for grid.
        """
        super().__init__(size)

        self.image = image
        self.items = items
        self.size = size

        self.grid = Grid(
            size=size,
            step=step,
        )

        self.update()

    def switch_grid(self):
        """Switch show grid."""
        MapImage.show_grid = not self.show_grid
        self.update()

    def update(self):
        """Update map image.
        
        Args:
            show_grid (bool): To show grid.
        """
        self.items.update()

        self.blit(self.image, self.get_rect())

        if self.items:
            self.items.draw(self)

        if self.show_grid:
            self.grid.draw(self)

    @classmethod
    def scaled(cls, filename, items, size=(1000, 1000), scale=None, step=None):
        """Draw map image.

        Args:
            filename (string): Filename with image.
            items (list): Map items.
            size (tuple): Map size.
            scale (float): Scale for image.
            step (float): Step for grid.
        Returns:
            pygame.Surface: Loaded image.
        """
        if cls.__cached_image:
            print("Reload from cache")
            return cls(cls.__cached_image, items, size=size, step=step)

        image = pygame.image.load(filename)

        if scale:
            image = pygame.transform.scale(
                image,
                (
                    int(image.get_width() * MAP_SCALE),
                    int(image.get_height() * MAP_SCALE),
                ),
            )

        cls.__cached_image = image
        return cls(image, items, size=size, step=step)
