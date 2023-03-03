import pygame
from .items import load_items
from .level import Level
from ..sprites.map import MapSprite


class Universe(Level):
    default_size = 5000, 5000

    def load(self, rect):
        hubble_deep_field = 127
        self.items = pygame.sprite.Group(*load_items(
            self.scale,
            self.size,
            step=hubble_deep_field,
        ))

        self.map_sprite = MapSprite(
            rect,
            items=self.items,
            starting_pos=self.starting_pos,
            size=self.size,
            grid_step=hubble_deep_field,
        )
