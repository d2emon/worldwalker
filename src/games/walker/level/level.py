import pygame
from .items import load_items
from ..sprites.map import MapSprite


class Level:
    default_size = 5000, 5000

    def __init__(self, scale):
        self.scale = scale

        self.size = self.default_size
        self.starting_pos = [int(i / 2) for i in self.size]
        self.step = 5

        self.items = pygame.sprite.Group()
        self.map_sprite = None

    @property
    def grid_step(self):
        return 100

    @property
    def max_pos(self):
        return [int(i / self.step) for i in self.size]

    @property
    def offset(self):
        return int(self.step / 2)

    @property
    def items_data(self):
        return load_items(self.scale, self.size)

    def get_items(self):
        items = list(self.items_data)
        for item in items:
            print(
                f"\t{item.rect.center}\t{item.rect.size}\t{item.name}",
                "\t[INVISIBLE]" if not item.visible else ''
            )
            if item.visible:
                yield item

    def load(self, rect):
        self.items = pygame.sprite.Group(*self.get_items())

        self.map_sprite = MapSprite(
            rect,
            items=self.items,
            starting_pos=self.starting_pos,
            size=self.size,
            grid_step=self.grid_step,
        )
