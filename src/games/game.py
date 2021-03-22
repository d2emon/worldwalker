import sys
from game.events import GameEvents
from windows.windows import Window


class Game:
    def __init__(self, window_config=None):
        window_config = window_config or {}

        self.window = Window(**window_config)
        self.events = GameEvents({
            GameEvents.QUIT: self.on_close,
        })

        self.window.events.listeners.append(self)

    @property
    def clock(self):
        return self.window.clock

    @property
    def is_showing(self):
        return self.window.is_showing

    @property
    def surface(self):
        return self.window.surface

    # Events
    def on_close(self, *args, **kwargs):
        self.window.close()

    # Phases
    def show(self):
        self.window.show()

    def update(self):
        self.window.update()

    def close(self):
        self.window.quit()
        sys.exit()

    # Main
    def __call__(self, *args, **kwargs):
        self.show()
        while self.is_showing:
            self.update()
        self.close()
