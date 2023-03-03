"""Main game screen.

Typical usage example:

  self.screen = MainScreen(self.window.get_rect())
  self.events.update(self.screen.events)

10^24
"""
import pygame
from events.game import GameEvents
from .items import load_items
from .player import Player
from ... import resource
from ...controls import CONTROLS
from ...sprites.map import MapSprite


class MainScreen(pygame.Surface):
    """Main screen for game

    Attributes:
        events (Events): Game events.
        sprites (Sprites): Screen sprites.
    """

    max_scale = 24
    min_scale = 0
    __size = 5000, 5000

    # Layers
    layer_bg = 0
    layer_map = 1
    layer_player = 3
    layer_controls = 4

    def __init__(self, rect, on_exit, game):
        """Initialize main screen.

        Args:
            rect (pygame.Rect): Main screen rect.
            on_exit (function): On exit event.
        """
        super().__init__((rect.width, rect.height))

        self.game = game
        self.rect = rect
        self.__scale = 24
        self.__x_vel = self.__y_vel = 0

        self.starting_pos = [int(i / 2) for i in self.__size]
        self.field_size = self.__size

        # Show loading
        # self.show_loading()

        # Create sprites

        self.items = None
        self.map_sprite = None

        self.sprites = pygame.sprite.LayeredUpdates()

        background = resource.main_screen_background(rect)
        self.sprites.add(background, layer=self.layer_bg)

        self.player = Player(
            screen_pos=rect.center,
            starting_pos=self.starting_pos,
            field_size=self.field_size,
        )
        self.sprites.add(self.player, layer=self.layer_player)

        self.coords_label = resource.coord_label(pygame.Rect(0, 0, 100, 100))
        self.sprites.add(self.coords_label, layer=self.layer_controls)

        self.order_label = resource.order_label(pygame.Rect(0, 100, 100, 100))
        self.sprites.add(self.order_label, layer=self.layer_controls)

        self.reload_map(self.scale)

        # Setup events

        control_events = { key: self.__move_handler(key) for key in CONTROLS }
        self.events = {
            GameEvents.KEY_DOWN: self.__key_event_handler({
                pygame.K_ESCAPE: on_exit,
                pygame.K_PAGEUP: self.handle_zoom_out,
                pygame.K_PAGEDOWN: self.handle_zoom_in,
                pygame.K_h: self.handle_reset,
                pygame.K_g: self.handle_switch_grid,
                **control_events,
            }),
            GameEvents.KEY_UP: self.__key_event_handler({
                **control_events,
            }),
        }

    def show_loading(self):
        """Show loading label."""
        print("Show Loading...")
        rect = self.game.window.get_rect()
        loading = resource.loading(rect)
        self.game.window.blit(loading.image, loading.rect)
        self.game.update()
        self.game.draw_bg()

    def reload_map(self, scale):
        """Reload level map

        Args:
            scale (int): Map scale.
        """

        # Show loading
        print("Loading...")
        self.show_loading()

        print(scale)
        if self.map_sprite:
            self.sprites.remove(self.map_sprite)

        self.items = pygame.sprite.Group(*load_items(scale, self.__size))
        for item in self.items:
            print(f"\t{item.rect.center}\t{item.rect.size}\t{item.name}")

        self.map_sprite = MapSprite(
            self.rect,
            items=self.items,
            starting_pos=self.starting_pos,
            size=self.field_size,
        )

        self.sprites.add(self.map_sprite, layer=self.layer_map)
        print("Loaded...")

    @property
    def scale(self):
        """Get scale.

        Returns:
            int: Current scale.
        """
        return self.__scale

    @scale.setter
    def scale(self, value):
        """set scale.

        Args:
            value (int): New scale.
        """
        if value < self.min_scale:
            self.__scale = self.min_scale
        elif value > self.max_scale:
            self.__scale = self.max_scale
        else:
            self.__scale = value

        self.reload_map(self.__scale)

    @property
    def x_vel(self):
        """Get x velocity.

        Returns:
            float: Velocity by x.
        """
        return self.__x_vel

    @x_vel.setter
    def x_vel(self, value):
        """Set x velocity.

        Args:
            value (float): Velocity by x.
        """
        if value is None:
            return

        self.__x_vel = value

    @property
    def y_vel(self):
        """Get y velocity.

        Returns:
            float: Velocity by y.
        """
        return self.__y_vel

    @y_vel.setter
    def y_vel(self, value):
        """Set y velocity.

        Args:
            value (float): Velocity by y.
        """
        if value is None:
            return

        self.__y_vel = value

    def update(self, *args, **kwargs):
        """On update event."""
        pos = self.player.move_by(self.x_vel, self.y_vel)
        if self.map_sprite:
            self.map_sprite.set_viewpoint(pos)

        # Update labels
        self.coords_label.pos = pos
        self.order_label.value = self.__scale

        self.sprites.update()
        self.sprites.draw(self)

    # Handler decorators

    def  __key_event_handler(self, events):
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

            self.x_vel = self.y_vel = 0

            for key, handler in events.items():
                if not keys[key]:
                    continue

                if not handler:
                    continue

                handler(key, *args, **kwargs)

        return events_handler

    def __move_handler(self, key):
        """Create move handler.
        
        Args:
            key (number): Pressed key.
        """

        def handler(*args, **kwargs):
            """Handle move player."""
            self.x_vel, self.y_vel = CONTROLS.get(key, (None, None))

        return handler

    # Handlers

    def handle_move(self, key, *args, **kwargs):
        """Handle move player.
        
        Args:
            key (number): Pressed key.
        """
        self.x_vel, self.y_vel = CONTROLS.get(key, (None, None))

    def handle_reset(self, *args, **kwargs):
        """Handle reset player."""
        self.player.reset_viewpoint()

    def handle_switch_grid(self, *args, **kwargs):
        """Handle switch grid."""
        if self.map_sprite:
            self.map_sprite.switch_grid()

    def handle_zoom_in(self, *args, **kwargs):
        """Handle zoom in."""
        self.scale -= 1

    def handle_zoom_out(self, *args, **kwargs):
        """Handle zoom out."""
        self.scale += 1
