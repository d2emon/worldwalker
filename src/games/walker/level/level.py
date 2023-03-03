import pygame
from .items import load_items
from ..sprites.map import MapSprite


class Level:
    default_size = 5000, 5000

    def __init__(self, scale):
        self.scale = scale

        self.size = self.default_size
        self.starting_pos = [int(i / 2) for i in self.size]

        self.items = pygame.sprite.Group()
        self.map_sprite = None

    def load(self, rect):
        self.items = pygame.sprite.Group(*load_items(self.scale, self.size))

        self.map_sprite = MapSprite(
            rect,
            items=self.items,
            starting_pos=self.starting_pos,
            size=self.size,
        )
