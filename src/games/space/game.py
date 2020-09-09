from windows.windows.game import GameWindow
from .main_surface import MainSurface


class Space(GameWindow):
    def on_init(self):
        super().on_init()

        self.screen = MainSurface(self.size, **self.config)
        self.events.update(self.screen.events)
