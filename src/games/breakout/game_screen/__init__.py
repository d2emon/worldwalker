import pygame
import random
from windows.screen import Screen
from .. import events
from .groups.bricks import Bricks
from .sprites.paddle import Paddle


class GameScreen(Screen):
    def __init__(self, size):
        super().__init__(size)
        self.rect = self.get_rect()

        self.player = Paddle((self.rect.centerx, 400))
        self.bricks = Bricks()

        self.sprites.add(self.player)

        self.events.update({
            events.EVENT_START: self.on_start,
            events.KEY_DOWN: self.on_key_down,
            events.KEY_UP: self.on_key_up,
        })

        self.events.emit(events.EVENT_START)

    def update(self, *args):
        super().update(self.rect, *args)
        self.bricks.update(self.player)

        if not self.player.has_started:
            return self.events.emit(events.EVENT_START)

        if not self.bricks:
            return self.events.emit(events.EVENT_WIN)

        if self.player.game_over:
            return self.events.emit(events.EVENT_LOOSE)

    def draw(self):
        super().draw()
        self.bricks.draw(self)

    # Events

    def on_start(self, *args, **kwargs):
        self.player.start((self.rect.center, (random.randint(-2, 2), 1)))
        self.sprites.add(self.player.ball)

    def on_key_down(self, *args, keys=None, **kwargs):
        if keys is None:
            return
        if self.player is None:
            return
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()

    def on_key_up(self, *args, keys=None, **kwargs):
        if keys is None:
            return
        self.player.stop()
