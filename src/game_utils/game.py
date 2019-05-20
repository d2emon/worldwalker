import sys
import pygame


DEFAULT = {
    'frame_rate': 60,
    'width': 640,
    'height': 480,
    'caption': 'Game',
}


class Game:
    STATE_EXIT = 0
    STATE_INITIALIZATION = 10
    STATE_PLAYING = 20
    STATE_GAME_OVER = 30

    def __init__(self, **config):
        self.state = self.STATE_INITIALIZATION

        self.frame_rate = config.get('frame_rate', DEFAULT['frame_rate'])
        self.width = config.get('width', DEFAULT['width'])
        self.height = config.get('height', DEFAULT['height'])
        self.caption = config.get('caption', DEFAULT['caption'])

        self.game_is_over = False
        self.objects = []

        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)

        self.surface = None

        self.clock = pygame.time.Clock()

        self.state = self.STATE_PLAYING

    def is_playing(self):
        return self.state != self.STATE_EXIT

    def play(self):
        while self.is_playing():
            self.handle_events()
            self.update()
            pygame.display.update()
            self.clock.tick(self.frame_rate)

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.state = self.STATE_EXIT
        # handler = self.event_handlers.get(event.type)
        # if handler is None:
        #     return
        # handler(event)

    @classmethod
    def end_game(cls):
        pygame.quit()
        sys.exit()

    def update(self):
        if self.surface is not None:
            self.screen.blit(self.surface, (0, 0))
