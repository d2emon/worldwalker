import sys
import pygame


DEFAULT = {
    'frame_rate': 60,
    # 'Back_image_filename': None,
    'width': 640,
    'height': 480,
    'caption': 'Game',
}


class Game:
    STATE_INITIALIZATION = 0
    STATE_MENU = 1
    STATE_PLAYING = 2
    STATE_GAME_OVER = 3
    STATE_EXIT = 4

    def __init__(self, **config):
        self.state = self.STATE_INITIALIZATION

        self.frame_rate = config.get('frame_rate', DEFAULT['frame_rate'])
        self.width = config.get('width', DEFAULT['width'])
        self.height = config.get('height', DEFAULT['height'])
        self.caption = config.get('caption', DEFAULT['caption'])

        self.game_over = False
        self.objects = []

        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.font.init()

        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)

        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 0, 0))
        self.background_pos = 0, 0

        self.clock = pygame.time.Clock()

        self.keydown_handlers = dict()
        self.keyup_handlers = dict()
        self.mouse_handlers = []

        self.event_handlers = {
            pygame.QUIT: self.exit_handler,
            pygame.KEYDOWN: self.keydown_handler,
            pygame.KEYUP: self.keyup_handler,
            pygame.MOUSEBUTTONDOWN: self.mouse_handler,
            pygame.MOUSEBUTTONUP: self.mouse_handler,
            pygame.MOUSEMOTION: self.mouse_handler,
        }
        self.state = self.STATE_PLAYING

    def play(self):
        while self.state != self.STATE_EXIT:
            # print(self.background, self.background_pos)
            self.surface.blit(self.background, self.background_pos)

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()

            self.clock.tick(self.frame_rate)

    def handle_events(self):
        for event in pygame.event.get():

            handler = self.event_handlers.get(event.type)
            if handler is not None:
                handler(event)

    def exit_handler(self, event):
        self.state = self.STATE_EXIT

    def keydown_handler(self, event):
        for handler in self.keydown_handlers.get(event.key, []):
            handler(event)

    def keyup_handler(self, event):
        for handler in self.keyup_handlers.get(event.key, []):
            handler(event)

    def mouse_handler(self, event):
        for handler in self.mouse_handlers:
            handler(event)

    @classmethod
    def end_game(cls):
        pygame.quit()
        sys.exit()

    def update(self):
        list(map(lambda item: item.update(), self.objects))

    def draw(self):
        list(map(lambda item: item.draw(self.surface), self.objects))
