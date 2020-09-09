import pygame
from pygame import Surface
from pygame.sprite import LayeredDirty
from .player import Player
from .world_map import BgMap
from .background import Background
from .grid import MapGrid


class MainSurface(Surface):
    MAP_POS = (0, 0)
    GRID_SIZE = 32
    CONTROLS = {
        pygame.K_LEFT: (-1, None),
        pygame.K_RIGHT: (1, None),
        pygame.K_UP: (None, -1),
        pygame.K_DOWN: (None, 1),
    }

    def __init__(self, size, **config):
        super().__init__(size)

        self.speed = [0, 0]

        self.my_font = pygame.font.SysFont('Sans', 16)

        rect = self.get_rect()

        self.background = Background()
        self.game_map = BgMap(*self.MAP_POS)
        self.map_grid = MapGrid(self.game_map.rect.width, self.game_map.rect.height, self.GRID_SIZE)
        self.hero = Player(rect.centerx, rect.centery)

        self.sprites = LayeredDirty((
            self.background,
            self.game_map,
            self.map_grid,
            self.hero,
        ))

        self.event_handlers = {
            pygame.KEYDOWN: [self.key_events],
            pygame.KEYUP: [self.key_events],
        }

    def update_map(self):
        self.game_map.x, self.game_map.y = self.MAP_POS

    def update(self):
        self.background.dirty = True

        self.game_map.set_speed(self.speed)

        self.sprites.update()
        self.sprites.draw(self)

        coords = "{}, {}".format(self.game_map.x, self.game_map.y)
        text_surface = self.my_font.render(coords, False, (0, 0, 0))
        self.blit(text_surface, (0, 0))

    def key_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.update_map()
            if event.key == pygame.K_g:
                self.map_grid.toggle()

        if event.key in self.CONTROLS.keys():
            self.movement_handler(event)

    def movement_handler(self, event):
        for i, value in enumerate(self.CONTROLS[event.key]):
            if value is None:
                continue
            if event.type == pygame.KEYDOWN:
                self.speed[i] = value
            if event.type == pygame.KEYUP:
                self.speed[i] = 0
