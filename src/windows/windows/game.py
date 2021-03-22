import pygame
from windows import states
from .window import Window


class GameWindow(Window):
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
            self.events.UPDATE: self.on_update,
            self.events.DRAW: self.on_draw,
            self.events.KEY_UP: self.on_key_up,
            self.events.KEY_DOWN: self.on_key_down,
        })

        self.state = states.INITIALIZATION
        self.game_is_over = False
        self.objects = []
        self.screen = None

    def set_screen(self, screen, state=None):
        if state is not None:
            self.state = state

        self.screen = screen
        self.events.events.update(self.screen.events.events)

    @property
    def is_showing(self):
        return self.state != states.EXIT

    def game_win(self):
        self.state = states.WIN

    def game_over(self):
        self.state = states.EXIT

    # Events

    def on_init(self):
        self.state = states.PLAYING

    def on_close(self, *args, **kwargs):
        self.game_over()

    def on_update(self, *args, **kwargs):
        if self.screen is not None:
            self.screen.update()

    def on_draw(self, *args, **kwargs):
        if self.screen is not None:
            self.screen.draw()
            self.surface.blit(self.screen, (0, 0))

    def on_key_up(self, *args, **kwargs):
        pass

    def on_key_down(self, *args, keys=None, **kwargs):
        if keys is None:
            return

        if pygame.K_ESCAPE in keys:
            self.game_over()
