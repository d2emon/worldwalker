import pygame
from events.window import WindowEvents


class GameEvents(WindowEvents):
    KEY = 'WINDOW.KEY'
    KEY_DOWN = 'WINDOW.KEYDOWN'
    KEY_UP = 'WINDOW.KEYUP'

    MOUSE_MOTION = 'WINDOW.MOUSEMOTION'
    MOUSE_BUTTON_DOWN = 'WINDOW.MOUSEBUTTONDOWN'
    MOUSE_BUTTON_UP = 'WINDOW.MOUSEBUTTONUP'

    GAME_MOUSE_MOTION = pygame.MOUSEMOTION
    GAME_MOUSE_BUTTON_DOWN = pygame.MOUSEBUTTONDOWN
    GAME_MOUSE_BUTTON_UP = pygame.MOUSEBUTTONUP

    QUIT = pygame.QUIT

    __EVENT_MAP = {
        pygame.KEYDOWN: KEY_DOWN,
        pygame.KEYUP: KEY_UP,
    }

    def __init__(self, events=None):
        super().__init__({
            pygame.KEYUP: self.on_key_event,
            pygame.KEYDOWN: self.on_key_event,

            pygame.MOUSEBUTTONDOWN: self.on_key_event,
            pygame.MOUSEBUTTONUP: self.on_key_event,
            pygame.MOUSEMOTION: self.on_key_event,
        })
        self.events.update(events or {})

    # Events
    def on_key_event(self, event_type, *args, **kwargs):
        self.emit(
            self.__EVENT_MAP.get(event_type),
            *args,
            **kwargs,
            keys=pygame.key.get_pressed(),
        )

    def on_mouse_event(self, event_type, *args, **kwargs):
        event = kwargs.get('event')
        self.emit(
            self.__EVENT_MAP.get(event_type),
            *args,
            **kwargs,
            pos=event.pos if event else None,
        )
