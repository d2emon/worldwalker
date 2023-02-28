"""Main game screen.

Typical usage example:

  self.screen = MainScreen(self.window.get_rect())
  self.events.update(self.screen.events)

10^24
"""
import pygame
from events.game import GameEvents
from .items import load_items
from ..controls import CONTROLS
from ..sprites.background import Background
from ..sprites.coord_label import CoordLabel
from ..sprites.map import MapSprite
from ..sprites.player import Player


class MainScreen(pygame.Surface):
    """Main screen for game

    Attributes:
        events (Events): Game events.
        sprites (Sprites): Screen sprites.
    """

    def __init__(self, rect, on_exit):
        """Initialize main screen.

        Args:
            rect (pygame.Rect): Main screen rect
        """
        super().__init__((rect.width, rect.height))

        starting_pos = (500, 500)
        layer_bg = 0
        layer_map = 1
        layer_player = 3
        layer_controls = 4

        # Create sprites
        
        self.items = pygame.sprite.Group(*load_items())
        self.sprites = pygame.sprite.LayeredUpdates()

        background = Background(rect)
        self.sprites.add(background, layer=layer_bg)

        self.map_sprite = MapSprite(rect, starting_pos, items=self.items)
        self.sprites.add(self.map_sprite, layer=layer_map)

        self.player = Player(rect, starting_pos)
        self.sprites.add(self.player, layer=layer_player)

        self.coords_label = CoordLabel()
        self.sprites.add(self.coords_label, layer=layer_controls)

        # Setup events
        control_events = { key: self.__on_control for key in CONTROLS }
        self.events = {
            GameEvents.KEY_DOWN: self.__on_key_event({
                pygame.K_ESCAPE: on_exit,
                pygame.K_h: self.player.reset_viewpoint,
                pygame.K_g: self.map_sprite.switch_grid,
                **control_events,
            }),
            GameEvents.KEY_UP: self.__on_key_event({
                **control_events,
            }),
        }

    def __on_control(self, key, *args, **kwargs):
        """Set player velocity.

        Args:
            key (number): Pressed key.
        """
        c = CONTROLS[key]
        if c[0] is not None:
            self.player.x_vel = c[0]
        if c[1] is not None:
            self.player.y_vel = c[1]

    def __on_key_event(self, events):
        """On key event decorator.

        Args:
            events (dict, optional): Dict of key event handlers.
        """

        def events_handler(*args, keys=None, **kwargs):
            """On key event.

            Args:
                keys (tuple, optional): Dict of key states.
            """
            if not keys:
                return

            self.player.x_vel = self.player.y_vel = 0

            for key, handler in events.items():
                if not keys[key]:
                    continue

                if not handler:
                    continue

                handler(key, *args, **kwargs)

        return events_handler

    def update(self, *args, **kwargs):
        """On update event."""

        self.player.move()
        self.map_sprite.set_viewpoint(self.player.pos)
        self.coords_label.pos = self.player.pos

        self.sprites.update()
        self.sprites.draw(self)
