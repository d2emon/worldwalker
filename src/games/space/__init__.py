#! /usr/bin/python
import pygame
import random
from games.game_utils import Game
from pygame import Surface
from pygame.sprite import Sprite, Group
from ..middleearth.player import Player

from genelib.scales import ObservableUniverse, SloanGreatWall, PerseusCetusSuperclusterComplex, EridanusSupervoid, VirgoSupercluster
from nestedscript import CosmicWall, GalaxyFilament, Supervoid, Supercluster


CONTROLS = {
    pygame.K_LEFT: (-100, None),
    pygame.K_RIGHT: (100, None),
    pygame.K_UP: (None, -100),
    pygame.K_DOWN: (None, 100),
}

GALAXY_COLOR = 255, 255, 255

MAX_X = 10000
MAX_Y = 10000


class CosmicWebItem(pygame.Surface):
    WALL_COLOR = 192, 192, 192
    FILAMENT_COLOR = 128, 128, 128
    VOID_COLOR = 0, 0, 0

    def __init__(self, item, position):
        self.item = item
        self.position = position
        super().__init__(self.item.size[:2], pygame.SRCALPHA, 32)

        self.update()

    def update(self):
        if isinstance(self.item, CosmicWall):
            color = self.WALL_COLOR
        elif isinstance(self.item, GalaxyFilament):
            color = self.FILAMENT_COLOR
        elif isinstance(self.item, Supervoid):
            color = self.VOID_COLOR
        elif isinstance(self.item, Supercluster):
            color = GALAXY_COLOR
        else:
            color = 255, 0, 0
            print(type(self.item))

        pygame.draw.ellipse(self, color, self.get_rect())


class GameUniverse(Sprite):
    COLOR = 32, 32, 32

    def __init__(self):
        web = [Supervoid() for _ in range(10000)] \
            + [CosmicWall() for _ in range(10000)] \
            + [GalaxyFilament() for _ in range(10000)] \
            + [Supercluster() for _ in range(10000)]

        self.universe = ObservableUniverse
        self.universe.web = [
            SloanGreatWall,
            PerseusCetusSuperclusterComplex,
            EridanusSupervoid,
            VirgoSupercluster,
        ] + web

        super().__init__()

        self.image = Surface(self.universe.size[:2])
        self.rect = self.image.get_rect()

        self.items = [CosmicWebItem(item, self.random_point()) for item in self.universe.web]

        self.first_update()

    def random_point(self):
        point = [random.randrange(self.universe.size[i]) for i in range(2)]
        return point

    def first_update(self):
        pygame.draw.ellipse(self.image, self.COLOR, self.rect)

        for item in self.items:
            # position = self.universe.size[0] / 2, self.universe.size[1] / 2
            position = item.position
            # print("Item is at ", position)
            self.image.blit(item, position)


class GamePlayer(Player):
    def update(self):
        self.rect = self.rect.move(self.speed)


class GameScreen(Surface):
    def __init__(self):
        self.universe = GameUniverse()
        self.hero = GamePlayer(self.universe.rect.centerx, self.universe.rect.centery)
        super().__init__((self.universe.rect.width, self.universe.rect.height))

        self.sprites = Group(self.universe, self.hero)

    @property
    def offset_position(self):
        # return self.position[0] - self.hero.rect.left, self.position[1] - self.hero.rect.top
        return 200 - self.hero.rect.left, 200 - self.hero.rect.top

    def update(self):
        self.sprites.update()

        if self.hero.rect.left < 0:
            self.hero.rect.left = 0
        if self.hero.rect.right > self.universe.rect.width:
            self.hero.rect.right = self.universe.rect.width
        if self.hero.rect.top < 0:
            self.hero.rect.top = 0
        if self.hero.rect.bottom > self.universe.rect.height:
            self.hero.rect.bottom = self.universe.rect.height

        self.sprites.draw(self)

    def show_position(self):
        print(self.universe.universe.size)
        print("Player is at ", self.hero.rect.left, self.hero.rect.top)
        print("Universe is at ", self.offset_position)


class MainSurface(Surface):
    def __init__(self, size, **config):
        super().__init__(size)

        self.screen = GameScreen()
        self.hero = self.screen.hero

        self.event_handlers = {
            pygame.KEYDOWN: (self.on_key_down, ),
            pygame.KEYUP: (self.on_key_up, ),
        }

    def on_key_down(self, event):
        if event.key in CONTROLS.keys():
            dx, dy = CONTROLS[event.key]
            if dx is not None:
                self.hero.speed = dx, self.hero.speed[1]
            if dy is not None:
                self.hero.speed = self.hero.speed[0], dy
        if event.key == pygame.K_SPACE:
            self.screen.show_position()

    def on_key_up(self, event):
        if event.key in CONTROLS.keys():
            dx, dy = CONTROLS[event.key]
            if dx is not None:
                self.hero.speed = 0, self.hero.speed[1]
            if dy is not None:
                self.hero.speed = self.hero.speed[0], 0

    def update(self):
        self.fill((0, 0, 0))
        self.screen.update()
        self.blit(self.screen, self.screen.offset_position)


class Space(Game):
    def __init__(self, **config):
        super().__init__(**config)

        self.surface = MainSurface((self.width, self.height), **config)

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_over()

        if self.surface is None:
            return
        handlers = self.surface.event_handlers.get(event.type)
        if handlers is None:
            return
        for handler in handlers:
            handler(event)

    def update(self):
        if self.surface is not None:
            self.surface.update()
        super().update()

    def game_over(self, *args):
        self.state = self.STATE_EXIT
