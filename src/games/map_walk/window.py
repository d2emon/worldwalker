import pygame
import sys


class Window:
    INIT = 'INIT'
    UPDATE = 'UPDATE'
    DRAW = 'DRAW'

    def __init__(
        self,
        caption='Game',
        fps=60,
        size=(800, 600),
    ):
        # Init pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.is_showing = False
        self.surface = None

        # Config
        self.caption = caption
        self.fps = fps
        self.size = size

        # Setup events
        self.events = {
            pygame.QUIT: self.on_close,
        }

    # Events
    def emit(self, event_type):
        emitter = self.events.get(event_type)
        if not emitter:
            return
        return emitter()

    def on_close(self):
        self.is_showing = False

    # Phases
    def show(self):
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.emit(self.INIT)
        self.is_showing = True

    def close(self):
        self.is_showing = False
        pygame.quit()
        sys.exit()

    def run(self):
        self.show()
        while self.is_showing:
            for event in pygame.event.get():
                self.emit(event.type)

            self.emit(self.UPDATE)
            self.emit(self.DRAW)

            pygame.display.update()

            self.clock.tick(self.fps)
        self.close()
