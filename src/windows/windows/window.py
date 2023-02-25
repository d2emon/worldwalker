import pygame
from game.events import GameEvents


class Window:
    INIT = GameEvents.INIT
    DRAW = GameEvents.DRAW
    KEYDOWN = GameEvents.KEY_DOWN
    UPDATE = GameEvents.UPDATE

    def __init__(
        self,
        caption='Game',
        fps=60,
        size=(800, 600),
    ):
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        # pygame.font.init()

        self.caption = caption
        self.fps = fps
        self.size = size
        self.clock = pygame.time.Clock()
        self.surface = None
        self.__is_showing = False
        self.events = GameEvents()

    @property
    def is_showing(self):
        return self.__is_showing

    @property
    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print ("QUIT")
                print ("QUIT")
                print ("QUIT")
                print (event.type)
            yield event

    def show(self):
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.events.init_window()
        self.__is_showing = True

    def update(self):
        self.events.process_events(self.game_events)
        pygame.display.update()
        self.clock.tick(self.fps)

    def close(self):
        self.__is_showing = False

    def quit(self):
        self.close()
        pygame.quit()
