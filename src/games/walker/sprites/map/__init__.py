"""Main map sprite.

Typical usage example:

  map_sprite = MapSprite(rect)
"""

import pygame
from ... import resource


class MapSprite(pygame.sprite.Sprite):
    """Main map sprite.

    Attributes:
        image (pygame.Surface): Sprite image.
        rect (pygame.Rect): Sprite rect.
        show_grid (bool): To show grid.
        starting_pos (tuple): Starting viewpoint.
        viewpoint (pygame.Rect): Source rect.
    """

    def __init__(
        self,
        rect,
        items=None,
        starting_pos=(500, 500),
        size=(1000, 1000),
        grid_step=100
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

        grid = resource.map_grid(size, grid_step, force=True)
        self.map_image = resource.map_sprite(size, grid, force=True)
        self.sprites = pygame.sprite.OrderedUpdates(
            resource.map_background(rect),
        )

        self.items = items
        self.map_image.update()

        self.starting_pos = starting_pos
        self.size = size
        self.viewpoint = pygame.Rect(rect)

        self.reset_viewpoint()

    @property
    def items(self):
        return self.map_image.items

    @items.setter
    def items(self, value):
        self.map_image.items = value

    @property
    def show_grid(self):
        return self.map_image.show_grid

    @show_grid.setter
    def show_grid(self, value):
        self.map_image.show_grid = value

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
        self.map_image.switch_grid()

    def update(self, *args, **kwargs):
        """Update map image."""
        self.sprites.update(*args, **kwargs)
        self.sprites.draw(self.image)

        self.image.blit(self.map_image, self.rect, self.viewpoint)
