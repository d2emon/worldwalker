from windows.windows import GameWindow
from .main_surface import MainSurface


class MiddleEarth(GameWindow):
    STATE_INITIALIZATION = 100
    STATE_MENU = 200
    STATE_PLAY = 300
    STATE_WIN = 400
    STATE_GAME_OVER = 500
    STATE_EXIT = 600

    def on_init(self):
        super().on_init()

        self.screen = MainSurface(self.size, **self.config)
        self.events.update(self.screen.events)
