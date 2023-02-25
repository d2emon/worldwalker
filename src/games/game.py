from events.game import GameEvents
from utils.game import Game as BaseGame


class Game:
    def __init__(self, window_config=None):
        window_config = window_config or {}

        self.__game = BaseGame(**window_config)
        self.events = GameEvents({
            GameEvents.QUIT: self.on_close,
        })

        # self.window.events.listeners.append(self)

    @property
    def clock(self):
        return self.__game.clock

    @property
    def is_showing(self):
        return self.__game.playing

    @property
    def surface(self):
        return self.__game.window

    # Events
    def on_close(self, *args, **kwargs):
        self.__game.playing = False

    # Phases
    def show(self):
        self.__game.show()

    def update(self):
        self.__game.update()

    def close(self):
        self.__game.quit()

    # Main
    def __call__(self, *args, **kwargs):
        self.show()

        while self.is_showing:
            self.update()

        self.close()
