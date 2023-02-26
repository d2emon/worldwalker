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
        show_grid (bool): To draw grid.
    """

    def __init__(self, image, step=None):
        """Initialize sprite.

        Args:
            image (pygame.Image): Base image.
            step (float): Step for grid.
        """
        super().__init__(image.get_size())

        self.__map_image = image

        self.show_grid = False

        self.grid = Grid(
            size=(200, 300),
            start=(210, 185),
            step=step,
        )

        self.update()

    def update(self, *args, **kwargs):
        """Update map image."""
        self.blit(self.__map_image, self.get_rect())

        if self.show_grid:
            self.grid.draw(self) 

    @classmethod
    def scaled(cls, filename, scale=1.0, step=None):
        """Draw map image.

        Args:
            filename (string): Filename with image.
            scale (float): Scale for image.
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

        return cls(image, step)
