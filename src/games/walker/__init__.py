"""Walk on map.

Typical usage example:

  game = MapWalk()
  game()
"""

import pygame
import config
from utils.game import Game
from .screens.main import MainScreen


class Walker(Game):
    """Main game class.

    Attributes:
        events (Events): Game events.
        screen (pygame.Surface): Current game screen.
    """

    # Game control event definition

    def __init__(self, caption=None, fps=None, size=None):
        """Initialize game.

        Args:
            caption (string, optional): Game window caption.
            fps (int, optional): FPS for game.
            size (tuple, optional): Game window size.
        """
        super().__init__(
            caption=caption or config.SCREEN.CAPTION,
            fps=fps or config.FPS,
            size=size or config.SCREEN.SIZE,
        )

        self.events.update({
            # self.events.INIT: self.on_init,
            # self.events.DRAW: self.on_draw,
            self.events.QUIT: self.on_quit,
            # self.events.UPDATE: self.on_update,
            # pygame.KEYDOWN: self.on_key_down
            # pygame.KEYUP: self.on_key_up
        })

        self.screen = None

    def start(self):
        """Initialize game.

        Initialize resource
        Initialize main screen
        Draw background
        """
        # Initialze font
        pygame.font.init()

        # Load screen
        self.screen = MainScreen(
            self.window.get_rect(),
            self.on_quit,
            self,
        )
        self.events.update(self.screen.events)

        self.draw_bg()

        super().start()

    def draw_bg(self):
        """Draw game background.

        Draw background surface on window
        """
        pygame.display.flip()

    def load(self):
        """Load game resources.

        Initialize Resource
        Load background
        Load main field
        Initialize labels
        """
        # Initialze font
        pygame.font.init()

    # Events

    def draw(self, *args, **kwargs):
        """Draw main window.

        Draw main field and update rect
        Draw labels and update rect
        """
        if self.screen:
            self.window.blit(self.screen, (0, 0))

        super().draw(*args, **kwargs)

    def update(self, *args, **kwargs):
        """Update game controls.

        Hadle key pressed
        Update background
        Update main field
        Update labels
        Check loose game
        """
        if self.screen:
            self.screen.update(*args, **kwargs)

        super().update(*args, **kwargs)

    def on_quit(self, *args, **kwargs):
        """Quit game."""
        self.quit()
