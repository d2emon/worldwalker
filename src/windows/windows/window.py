import pygame
import sys
from events import Events


class Window:
    INIT = 'WINDOW.INIT'
    UPDATE = 'WINDOW.UPDATE'
    DRAW = 'WINDOW.DRAW'

    KEY = 'WINDOW.KEY'
    KEYDOWN = 'WINDOW.KEYDOWN'
    KEYUP = 'WINDOW.KEYUP'

    MOUSEMOTION = 'WINDOW.MOUSEMOTION'
    MOUSEBUTTONDOWN = 'WINDOW.MOUSEBUTTONDOWN'
    MOUSEBUTTONUP = 'WINDOW.MOUSEBUTTONUP'

    __EVENT_MAP = {
        pygame.KEYDOWN: KEYDOWN,
        pygame.KEYUP: KEYUP,
    }

    def __init__(
        self,
        caption='Game',
        fps=60,
        size=(800, 600),
    ):
        # Init pygame
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        # pygame.font.init()

        self.clock = pygame.time.Clock()
        self.__is_showing = False
        self.surface = None

        # Config
        self.caption = caption
        self.fps = fps
        self.size = size

        # Setup events
        self.events = Events({
            pygame.QUIT: self.on_close,

            pygame.KEYUP: self.on_key_event,
            pygame.KEYDOWN: self.on_key_event,

            pygame.MOUSEBUTTONDOWN: self.on_key_event,
            pygame.MOUSEBUTTONUP: self.on_key_event,
            pygame.MOUSEMOTION: self.on_key_event,
        })

    @property
    def is_showing(self):
        return self.__is_showing

    # Events
    def on_close(self, *args, **kwargs):
        self.__is_showing = False

    def on_key_event(self, event_type, *args, **kwargs):
        self.events.emit(
            self.__EVENT_MAP.get(event_type),
            *args,
            **kwargs,
            keys=pygame.key.get_pressed(),
        )

    def on_mouse_event(self, event_type, *args, **kwargs):
        event = kwargs.get('event')
        self.events.emit(
            self.__EVENT_MAP.get(event_type),
            *args,
            **kwargs,
            pos=event.pos if event else None,
        )

    # Phases
    def show(self):
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.events.emit(self.INIT)
        self.__is_showing = True

    def close(self):
        self.__is_showing = False
        pygame.quit()
        sys.exit()

    def run(self):
        self.show()
        while self.is_showing:
            for event in pygame.event.get():
                self.events.emit(event.type, event=event)

            self.events.emit(self.UPDATE)
            self.events.emit(self.DRAW)

            pygame.display.update()

            self.clock.tick(self.fps)
        self.close()
