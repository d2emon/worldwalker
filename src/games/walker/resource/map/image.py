"""Main map image.

Typical usage example:

  map_image = MapImage(image)
"""

import pygame


class MapImage(pygame.Surface):
    """Main map sprite.

    Attributes:
        grid (Grid): Grid for image.
    """

    show_grid = True

    def __init__(self, image, size=(1000, 1000), grid=None):
        """Initialize sprite.

        Args:
            image (pygame.Image): Base image.
            size (tuple): Map size.
            grid (pygame.Surface): Map grid
        """
        super().__init__(size)

        self.image = image
        self.items = pygame.sprite.Group()
        self.size = size

        self.grid = grid

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
            self.blit(self.grid, self.get_rect())

    @classmethod
    def scaled(cls, image, size=(1000, 1000), scale=None, grid=None):
        """Draw map image.

        Args:
            image (pygame.Surface): Map image.
            size (tuple): Map size.
            scale (float): Scale for image.
            grid (pygame.Surface): Map grid
        Returns:
            pygame.Surface: Loaded image.
        """
        if scale is None:
            return cls(image, size=size, grid=grid)

        scaled_image = pygame.transform.scale(
            image,
            (
                int(image.get_width() * scale),
                int(image.get_height() * scale),
            ),
        )

        return cls(scaled_image, size=size, grid=grid)
