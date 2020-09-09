from windows.windows import GameWindow
from windows.controls import TextObject
from . import states
from .screens import MenuScreen, GameScreen


class Breakout(GameWindow):
    @property
    def is_showing(self):
        return self.state != states.EXIT

    # States
    def game_menu(self):
        self.set_screen(
            MenuScreen(self.size),
            states.MENU,
        )
        self.screen.add_menu_item('PLAY', self.on_select_play)
        self.screen.add_menu_item('QUIT', self.on_select_quit)

    def game_play(self):
        self.set_screen(
            GameScreen(self.size),
            states.PLAYING,
        )
        self.screen.events.events[GameScreen.EVENT_WIN] = self.on_win
        self.screen.events.events[GameScreen.EVENT_LOOSE] = self.on_loose

    def game_over(self):
        self.state = states.EXIT

    def game_win(self):
        self.state = states.WIN
        self.game_over()

    # Events

    def on_init(self, *args, **kwargs):
        super().on_init()
        self.game_menu()

    def on_select_play(self, *args, **kwargs):
        self.game_play()

    def on_select_quit(self, *args, **kwargs):
        self.game_over()

    def on_win(self, *args, **kwargs):
        TextObject.show_message(self, "YOU WIN!!!", center=True)
        return self.game_win()

    def on_loose(self, *args, **kwargs):
        TextObject.show_message(self, "YOU LOOSE!!!", center=True)
        return self.game_over()
