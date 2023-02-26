from utils.state_game import StateGame
from windows.controls import TextObject
from . import events, states
from .menu_screen import MenuScreen
from .game_screen import GameScreen


class Breakout(StateGame):
    def game_menu(self):
        self.set_screen(
            MenuScreen(self.size),
            states.MENU,
            events={
                events.MENU_PLAY: self.on_select_play,
                events.MENU_QUIT: self.on_select_quit,
            },
        )

    def game_play(self):
        self.set_screen(
            GameScreen(self.size),
            states.PLAYING,
            events={
                events.EVENT_WIN: self.on_win,
                events.EVENT_LOOSE: self.on_loose,
            },
        )

    # Events

    def on_init(self, *args, **kwargs):
        super().on_init()
        self.game_menu()

    def on_select_play(self, *args, **kwargs):
        self.game_play()

    def on_select_quit(self, *args, **kwargs):
        self.stop()

    def on_win(self, *args, **kwargs):
        TextObject.show_message(self, "YOU WIN!!!", center=True)
        return self.game_win()

    def on_loose(self, *args, **kwargs):
        TextObject.show_message(self, "YOU LOOSE!!!", center=True)
        return self.stop()
