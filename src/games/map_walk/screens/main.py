"""Main game screen.

Typical usage example:

  self.screen = MainScreen(self.window.get_rect())
  self.events.update(self.screen.events)
"""
import pygame
import config
from pygame.sprite import LayeredUpdates
from events.game import GameEvents
from ..sprites.map import MapSprite, draw_map
from ..sprites.player import Player
from ..red_lands import PLAYER_SPEED



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

        map_image = draw_map(
            config.MAP_FILE,
            config.MAP_SCALE,
            config.SCALE,
        )
        self.map_sprite = MapSprite(
            map_image,
            rect,
            config.VIEWPOINT,
            config.SCALE * config.TIME_SCALE,
        )
        self.add(self.map_sprite, layer=0)

        self.player = Player(
            rect.center,
            scale=config.SCALE,
            speed=PLAYER_SPEED,
        )
        self.add(self.player, layer=1)


class MainScreen(pygame.Surface):
    """Main screen for game

    Attributes:
        events (Events): Game events.
        sprites (Sprites): Screen sprites.
    """

    def __init__(self, rect):
        """Initialize main screen.

        Args:
            rect (pygame.Rect): Main screen rect
        """
        super().__init__((rect.width, rect.height))

        self.sprites = Sprites(rect)

        self.events = {
            GameEvents.UPDATE: self.__on_update,
            GameEvents.KEY_DOWN: self.__on_key_down,
        }

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

    def __on_key_down(self, *args, keys=None, **kwargs):
        """On key down event.

        Args:
            keys (tuple, optional): Dict of key states.
        """
        if not keys:
            return

        speed = self.player.speed
        if keys[pygame.K_LEFT]:
            self.map_sprite.move(-speed, 0)
        if keys[pygame.K_RIGHT]:
            self.map_sprite.move(speed, 0)
        if keys[pygame.K_UP]:
            self.map_sprite.move(0, -speed)
        if keys[pygame.K_DOWN]:
            self.map_sprite.move(0, speed)

    def __on_update(self, *args, **kwargs):
        """On update event."""
        self.sprites.update()
        self.sprites.draw(self)
