from games.game_utils import Game
from .screens import MenuScreen, GameScreen


class Breakout(Game):
    STATE_INITIALIZATION = 100
    STATE_MENU = 200
    STATE_PLAY = 300
    STATE_WIN = 400
    STATE_GAME_OVER = 500
    STATE_EXIT = 600

    def __init__(self, **config):
        super().__init__(**config)

        self.menu_items = (
            ('PLAY', self.show_game),
            ('QUIT', self.game_over),
        )

        self.mouse_handlers = []
        self.keydown_handlers = []
        self.keyup_handlers = []

        self.event_handlers = dict()
        self.show_menu()

    def update(self):
        if self.surface is not None:
            self.surface.update()
        super().update()

    def handle_event(self, event):
        super().handle_event(event)

        if self.surface is None:
            return
        handlers = self.surface.event_handlers.get(event.type)
        if handlers is None:
            return
        for handler in handlers:
            handler(event)

    def show_menu(self, *args):
        self.state = self.STATE_MENU
        self.surface = MenuScreen((self.width, self.height), self.menu_items)

    def show_game(self, *args):
        self.state = self.STATE_PLAYING
        events = {
            GameScreen.EVENT_WIN: self.game_win,
            GameScreen.EVENT_LOOSE: self.game_over,
        }
        self.surface = GameScreen((self.width, self.height), events)

    def game_win(self, *args):
        self.state = self.STATE_WIN
        self.game_over()

    def game_over(self, *args):
        self.state = self.STATE_EXIT
