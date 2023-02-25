from utils.state_game import StateGame
from .main_surface import MainSurface


class Space(StateGame):
    def on_init(self):
        super().on_init()

        self.screen = MainSurface(self.size, **self.config)
        self.update_events(self.screen.events)
