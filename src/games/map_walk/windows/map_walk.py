import config
import pygame
from games.map_walk.screens.main import MainScreen
from windows.windows.window import Window


class MapWalkWindow(Window):
    def __init__(self):
        super().__init__(
            caption=config.SCREEN.CAPTION,
            fps=config.FPS,
            size=config.SCREEN.SIZE,
        )

        self.events.events[self.INIT] = self.on_init

        self.screen = None

    def on_init(self, *args, **kwargs):
        self.screen = MainScreen(self.surface.get_rect())
        self.events.events.update(self.screen.events)
        self.events.events[self.DRAW] = self.on_draw
        self.events.events[pygame.QUIT] = self.on_quit

    def on_draw(self, *args, **kwargs):
        self.surface.blit(self.screen, (0, 0))

    def on_quit(self, *args, **kwargs):
        self.quit()
