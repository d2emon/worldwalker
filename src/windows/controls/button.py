import pygame
from pygame.sprite import Sprite
from events import Events
from .text_object import TextObject


class Button(Sprite):
    class States:
        NORMAL = 0
        HOVER = 1
        PRESSED = 2

    class EventTypes:
        CLICK = 'CLICK'
        HOVER = 'HOVER'
        LEAVE = 'LEAVE'
        PRESS = 'PRESS'

    def __init__(
        self,
        rect,
        text,
        on_click=lambda *args, **kwargs: None,
        padding=5,
        font=None,
    ):
        super().__init__()
        self.image = pygame.Surface((rect.width, rect.height))
        self.rect = rect

        self.text = TextObject(
            x=padding,
            y=padding,
            text=lambda: text,
            font=font,
        )

        self.state = self.States.NORMAL
        self.events = Events({
            pygame.MOUSEMOTION: self.on_mouse_move,
            pygame.MOUSEBUTTONDOWN: self.on_mouse_down,
            pygame.MOUSEBUTTONUP: self.on_mouse_up,
            self.EventTypes.CLICK: on_click,
            self.EventTypes.HOVER: self.on_hover,
            self.EventTypes.LEAVE: self.on_leave,
            self.EventTypes.PRESS: self.on_press,
        })

    def draw(self, state):
        if state == self.States.NORMAL:
            self.image.fill((255, 255, 255))
        elif state == self.States.HOVER:
            self.image.fill((0, 255, 255))
        elif state == self.States.PRESSED:
            self.image.fill((0, 0, 255))

    def update(self, *args):
        self.draw(self.state)
        self.text.draw(self.image)

    # Events

    def on_mouse_move(self, *args, **kwargs):
        pos = kwargs.get('pos', (0, 0))
        if not self.rect.collidepoint(pos):
            return self.events.emit(self.EventTypes.LEAVE, *args, **kwargs)

        if self.state == self.States.PRESSED:
            return

        self.events.emit(self.EventTypes.HOVER, *args, **kwargs)

    def on_mouse_down(self, *args, **kwargs):
        pos = kwargs.get('pos', (0, 0))
        if not self.rect.collidepoint(pos):
            return

        self.events.emit(self.EventTypes.PRESS, *args, **kwargs)

    def on_mouse_up(self, *args, **kwargs):
        if self.state != self.States.PRESSED:
            return

        self.events.emit(self.EventTypes.CLICK, *args, **kwargs)
        self.events.emit(self.EventTypes.HOVER, *args, **kwargs)

    def on_hover(self, *args, **kwargs):
        self.state = self.States.HOVER

    def on_leave(self, *args, **kwargs):
        self.state = self.States.NORMAL

    def on_press(self, *args, **kwargs):
        self.state = self.States.PRESSED
