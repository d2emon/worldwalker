"""Main game screen.

Typical usage example:

  self.screen = MainScreen(self.window.get_rect())
  self.events.update(self.screen.events)
"""
import pygame
from pygame.sprite import LayeredUpdates
import config
from events.game import GameEvents
from ..controls import CONTROLS
from ..sprites.coord_label import CoordLabel
from ..sprites.map import MapSprite
from ..sprites.map_image import MapImage
from ..sprites.player import Player


class Sprites(LayeredUpdates):
    """Sprites for main screen.
    
    Attributes:
      map_sprite (MapSprite): Map sprite.
      player (Player): Player sprite.
    """

    def __init__(self, rect):
        """Intialize main sprites

        Args:
            rect (pygame.Rect): Screen rect
        """
        super().__init__()

        # self.bg = Background((self.window.get_width(), self.window.get_height()))
        # self.add(image, layer=0)

        map_image = MapImage.scaled(
            config.MAP_FILE,
            None, # config.MAP_SCALE,
            config.SCALE,
        )
        self.map_sprite = MapSprite(
            map_image,
            rect,
            config.VIEWPOINT,
            config.SCALE * config.TIME_SCALE,
        )
        self.add(self.map_sprite, layer=1)

        self.player = Player(
            rect.center,
            scale=config.SCALE,
        )
        self.add(self.player, layer=2)

        self.coords = CoordLabel()
        self.add(self.coords, layer=3)


class MainScreen(pygame.Surface):
    """Main screen for game

    Attributes:
        events (Events): Game events.
        sprites (Sprites): Screen sprites.
    """

    def __init__(self, rect, on_exit):
        """Initialize main screen.

        Load game resource: background
        Load game resource: main field
        Initialize labels

        Args:
            rect (pygame.Rect): Main screen rect
        """
        super().__init__((rect.width, rect.height))

        self.sprites = Sprites(rect)

        control_events = { key: self.__on_control for key in CONTROLS }
        self.events = {
            # GameEvents.UPDATE: self.__on_update,
            GameEvents.KEY_DOWN: self.__on_key_event({
                pygame.K_ESCAPE: on_exit,
                pygame.K_h: self.map_sprite.reset_viewpoint,
                pygame.K_g: self.map_sprite.switch_grid,
                **control_events,
            }),
            GameEvents.KEY_UP: self.__on_key_event({
                **control_events,
            }),
        }

        self.x_vel = self.y_vel = 0
        # TODO: Move to player

    @property
    def map_sprite(self):
        """Getter for map sprite.

        Returns:
            MapSprite: Map sprite
        """
        return self.sprites.map_sprite

    @property
    def player(self):
        """Getter for player sprite.

        Returns:
            Player: Player sprite.
        """
        return self.sprites.player

    def __on_control(self, key, *args, **kwargs):
        c = CONTROLS[key]
        if c[0] is not None:
            self.x_vel = c[0]
        if c[1] is not None:
            self.y_vel = c[1]

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

            # speed = self.player.speed
            self.x_vel = self.y_vel = 0

            for key, handler in events.items():
                if not keys[key]:
                    continue

                if not handler:
                    continue

                handler(key)

        return events_handler

    def update(self, *args, **kwargs):
        """On update event."""

        self.map_sprite.move(self.x_vel, self.y_vel)

        self.sprites.coords.x = self.map_sprite.viewpoint.centerx
        self.sprites.coords.y = self.map_sprite.viewpoint.centery

        self.sprites.update()
        self.sprites.draw(self)
