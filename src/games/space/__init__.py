#! /usr/bin/python
import config
import pygame
import random
from games.middleearth.player import Player
# from bgmap import BgMap
# from background import Background
# from grid import MapGrid
from pygame.time import Clock

from scales.yotta import ObservableUniverse, SloanGreatWall, PerseusCetusSuperclusterComplex, EridanusSupervoid, VirgoSupercluster
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


class GameUniverse(pygame.Surface):
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

        super().__init__(self.universe.size[:2])

        self.position = -self.universe.size[0] / 2, -self.universe.size[1] / 2
        # self.universe_rect = (0, 0, self.universe.size[0], self.universe.size[1])

        # bg = Background((config.WIN_WIDTH, config.WIN_HEIGHT))

        # game_map = BgMap(*config.MAP_POS)

        self.items = [CosmicWebItem(item, self.random_point()) for item in self.universe.web]

        self.update()

    def make_position(self, position):
        return [self.position[i] - position[i] for i in range(2)]

    def random_point(self):
        point = [random.randrange(self.universe.size[i]) for i in range(2)]
        return point

    def update(self):
        pygame.draw.ellipse(self, self.COLOR, self.get_rect())

        for item in self.items:
            # position = self.universe.size[0] / 2, self.universe.size[1] / 2
            position = item.position
            # print("Item is at ", position)
            self.blit(item, position)

        # bg.draw(screen)

        # game_map.update(xvel, yvel)
        # game_map.draw(screen)

        # if show_grid:
        #     map_grid.draw(screen)


class GameHero:
    def __init__(self):
        self.hero = Player(*config.PLAYER_POS)
        self.velocity = [0, 0]
        self.position = [0, 0]

    def update(self):
        # print(self.velocity, self.position)
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        if self.position[0] < -MAX_X:
            self.position[0] = MAX_X
        if self.position[1] < -MAX_Y:
            self.position[1] = MAX_Y
        if self.position[0] > MAX_X:
            self.position[0] = -MAX_X
        if self.position[1] > MAX_Y:
            self.position[1] = -MAX_Y

    def draw(self, screen):
        self.hero.draw(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode(config.DISPLAY)
    pygame.display.set_caption(config.TITLE)

    # pygame.font.init()
    # myfont = pygame.font.SysFont('Sans', 16)

    universe = GameUniverse()
    hero = GameHero()

    # show_grid = False
    # map_grid = MapGrid(game_map.rect.width, game_map.rect.height, config.GRID_SIZE)

    timer = Clock()

    while True:
        for event in pygame.event.get():
            event_exit(event)
            hero.velocity = event_move(event, hero.velocity)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                # game_map.x = config.MAP_POS[0]
                # game_map.y = config.MAP_POS[1]
                pass
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                # show_grid = not show_grid
                pass
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print(universe.universe.size)
                print("Player is at ", hero.position)
                print("Universe is at ", (-hero.position[0], -hero.position[1]))

        hero.update()
        # universe.update()

        screen.fill((0, 0, 0))
        screen.blit(universe, universe.make_position(hero.position))

        hero.draw(screen)

        # coords = "{}, {}".format(game_map.x, game_map.y)
        # text_surface = myfont.render(coords, False, (0, 0, 0))
        # screen.blit(text_surface, (0, 0))

        pygame.display.update()
        timer.tick(24)


def event_exit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit("QUIT")
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        raise SystemExit("QUIT")


def event_move(event, velocity):
    if event.type == pygame.KEYDOWN and event.key in CONTROLS.keys():
        c = CONTROLS[event.key]
        if c[0] is not None:
            velocity[0] = c[0]
        if c[1] is not None:
            velocity[1] = c[1]

    if event.type == pygame.KEYUP and event.key in CONTROLS.keys():
        c = CONTROLS[event.key]
        if c[0] is not None:
            velocity[0] = 0
        if c[1] is not None:
            velocity[1] = 0
    return velocity


if __name__ == "__main__":
    main()
