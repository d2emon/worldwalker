"""Base level class."""

import pygame
import random
from .items import load_items
from ..sprites.map import MapSprite


class Level:
    """Base level class.

    Attributes:
        default_size (tuple): Default level size.
        items (pygame.sprite.Group): Map items.
        map_sprite (pygame.sprite.Sprite): Map sprite.
        scale (int): Map scale.
        size (tuple): Map size.
        starting_pos (tuple): Player starting pos.
        step (int): Map items grid.
    """

    cell = 100
    default_size = 5000, 5000
    zoom_size = 100, 100

    def __init__(self, scale):
        """Initialize level.

        Args:
            scale (int): Level scale.
        """
        self.scale = scale

        self.size = self.default_size
        self.starting_pos = [int(i / 2) for i in self.size]
        self.step = 5

        self.items = pygame.sprite.Group()
        self.map_sprite = None

    @property
    def grid_step(self):
        """Get map grid step.

        Returns:
            int: Map grid step.
        """
        return self.cell

    @property
    def max_pos(self):
        """Get map item max pos.

        Returns:
            tuple: Map item max pos.
        """
        return [int(i / self.step) for i in self.size]

    @property
    def offset(self):
        """Get map item offset.

        Returns:
            int: Map item offset.
        """
        return int(self.step / 2)

    @property
    def items_data(self):
        """Get map items.

        Yields:
            Item: Map item.
        """
        yield from load_items(self.scale, self.size)

    @property
    def map_items(self):
        """Get map items.

        Yields:
            Item: Visible map item.
        """
        items = list(self.items_data)
        for item in items:
            print(
                f"\t{str(item.rect.center):<15}"
                f"{str(item.rect.size):<15}"
                f"{item.name:<50}"
                f"{'[INVISIBLE]' if not item.visible else ''}"
            )
            if item.visible:
                yield item

    def random_point(self):
        """Get random map point.

        Returns:
            list: Random map point.
        """
        return [
            random.randrange(0, self.max_pos[i]) * self.step + self.offset
            for i in range(2)
        ],

    def load(self, rect):
        """Load level map.

        Args:
            rect (pygame.Rect): Map rect.
        """
        self.items = pygame.sprite.Group(*self.map_items)

        self.map_sprite = MapSprite(
            rect,
            items=self.items,
            starting_pos=self.starting_pos,
            size=self.size,
            grid_step=self.grid_step,
        )
