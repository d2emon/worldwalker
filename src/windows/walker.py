import pygame
import config
from games.map_walk.window import Window
from player import Player
from bgmap import BgMap
from background import Background
from grid import MapGrid


class WalkerWindow(Window):
    CONTROLS = {
        pygame.K_LEFT: (-1, None),
        pygame.K_RIGHT: (1, None),
        pygame.K_UP: (None, -1),
        pygame.K_DOWN: (None, 1),
    }

    def __init__(self):
        super().__init__(
            caption=config.SCREEN_CAPTION,
            # fps=config.FPS,
            fps=24,
            size=config.SCREEN_SIZE,
        )

        self.events[pygame.KEYDOWN] = self.on_key_down
        self.events[pygame.KEYUP] = self.on_key_up

        self.screen = None

        self.my_font = None
        self.bg = None
        self.game_map = None
        self.hero = None
        self.map_grid = None

        self.x_vel = self.y_vel = 0
        self.show_grid = False

    def on_key_down(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.close()
        for key in self.CONTROLS.keys():
            if keys[key]:
                c = self.CONTROLS[key]
                if c[0] is not None:
                    self.x_vel = c[0]
                if c[1] is not None:
                    self.y_vel = c[1]
        if keys[pygame.K_h]:
            self.game_map.x = config.MAP_POS[0]
            self.game_map.y = config.MAP_POS[1]
        if keys[pygame.K_g]:
            self.show_grid = not self.show_grid

    def on_key_up(self):
        keys = pygame.key.get_pressed()
        for key in self.CONTROLS.keys():
            if keys[key]:
                c = self.CONTROLS[key]
                if c[0] is not None:
                    self.x_vel = 0
                if c[1] is not None:
                    self.y_vel = 0

    def on_init(self):
        # self.screen = MainScreen(self.surface.get_rect())
        # self.events.update(self.screen.events)
        # self.events[self.DRAW] = self.on_draw

        pygame.font.init()
        self.my_font = pygame.font.SysFont('Sans', 16)

        self.bg = Background((self.surface.get_width(), self.surface.get_height()))

        self.game_map = BgMap(*config.MAP_POS)
        self.hero = Player(*config.PLAYER_POS)

        self.map_grid = MapGrid(self.game_map.rect.width, self.game_map.rect.height, config.GRID_SIZE)

    def on_draw(self):
        # self.surface.blit(self.screen, (0, 0))

        self.bg.draw(self.surface)

        self.game_map.update(self.x_vel, self.y_vel)
        self.game_map.draw(self.surface)

        if self.show_grid:
            self.map_grid.draw(self.surface)

        self.hero.draw(self.surface)

        coords = "{}, {}".format(self.game_map.x, self.game_map.y)
        text_surface = self.my_font.render(coords, False, (0, 0, 0))
        self.surface.blit(text_surface, (0, 0))
