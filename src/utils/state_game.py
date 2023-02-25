import pygame
from windows import states
from .game import Game


class StateGame(Game):
    STATE_EXIT = states.EXIT
    STATE_GAME_OVER = states.GAME_OVER
    STATE_INITIALIZATION = states.INITIALIZATION
    STATE_PLAYING = states.PLAYING
    STATE_WIN = states.WIN

    def __init__(
        self,
        caption='Game',
        fps=60,
        size=(640, 480),
        **config,
    ):
        super().__init__(
            caption=caption,
            fps=fps,
            size=size,
        )
        self.config = config
        self.events.update({
            self.events.INIT: self.on_init,
            # self.events.UPDATE: self.on_update,
            # self.events.DRAW: self.on_draw,
            self.events.KEY_UP: self.on_key_up,
            self.events.KEY_DOWN: self.on_key_down,
        })

        self.game_is_over = False
        self.screen = None
        self.state = self.STATE_INITIALIZATION
        self.objects = []

    def set_screen(self, screen, state=None):
        if state is not None:
            self.state = state

        self.screen = screen
        self.events.update(self.screen.events.handlers)

    @property
    def playing(self):
        return self.state != self.STATE_EXIT

    def game_over(self):
        self.state = self.STATE_EXIT

    def game_start(self):
        self.state = self.STATE_PLAYING

    def game_win(self):
        self.state = self.STATE_WIN

    # Events

    def on_close(self, *args, **kwargs):
        self.game_over()

    def on_draw(self, *args, **kwargs):
        if self.screen is None:
            return

        self.screen.draw()
        self.window.blit(self.screen, (0, 0))

    def on_init(self, *args, **kwargs):
        self.game_start()

    def on_key_down(self, *args, keys=None, **kwargs):
        if keys is None:
            return

        if pygame.K_ESCAPE in keys:
            self.game_over()

    def on_key_up(self, *args, **kwargs):
        pass

    def on_update(self, *args, **kwargs):
        if self.screen is None:
            return

        self.screen.update()

    #

    def update_events(self, events):
        pass
