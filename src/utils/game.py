"""Base Game class.

Typical usage example:

  game = Game()
  game()
"""

import sys
import pygame
from events.game import GameEvents


class Game:
    """Base game abstraction.

    Attributes:
        caption (str, optional): Window caption
        clock (pygame.time.Clock): Game timer
        fps (int): FPS for game
        playing (bool): Game is playing
        size (tuple, optional): Window size
        window (pygame.Window): Game window
    """

    def __init__(self, size=(800, 600), caption="Game", fps=60):
        """Initialize game window.

        Args:
            caption (str, optional): Window caption. Defaults to "Game".
            fps (int, optional): FPS for game. Defaults to 60.
            size (tuple, optional): Window size. Defaults to (800, 600).
        """
        # pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        # pygame.font.init()

        self.caption = caption
        self.clock = pygame.time.Clock()
        self.events = GameEvents({
            GameEvents.DRAW: self.draw,
            GameEvents.QUIT: self.quit,
            GameEvents.UPDATE: self.update,
        })
        self.fps = fps
        self.__playing = False
        self.size = size
        # self.surface = None
        self.window = None

    @property
    def playing(self):
        return self.__playing

    @playing.setter
    def playing(self, value):
        self.__playing = value

    def start(self):
        self.playing = True

    def stop(self):
        self.playing = False

    def draw(self, *args, **kwargs):
        """Draw game screen."""
        pygame.display.flip()

    def quit(self, *args, **kwargs):
        """Close game window."""
        self.stop()

        pygame.quit()
        sys.exit()

    def show(self):
        """Show game window."""
        self.window = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.events.init_window()
        self.start()

    def update(self, *args, **kwargs):
        """Update game."""
        # self.events.process_events(self.game_events)
        # pygame.display.update()
        self.clock.tick(self.fps)

    def __call__(self, *args, **kwargs):
        """Run main game loop."""
        self.show()

        while self.playing:
            self.events.process_events(event for event in pygame.event.get())
            # self.update()
            # self.draw()
            self.clock.tick(self.fps)

        # To perform exit
