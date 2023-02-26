"""Game button.

Typical usage example:

  button = Button(
    (0, 0, 100, 100),
    "Caption",
    on_click,
    padding=5,
  )
"""

import pygame
from pygame.sprite import Sprite
from events import Events
from .text_object import TextObject


class Button(Sprite):
    """Game button.

    Attributes:
        events (Events): Button events.
        state (int): Button state.
        text (TextObject): Text sprite with button caption.
        on_click (function): Button on_click event.
    """

    class States:
        """Game button states."""
        NORMAL = 0
        HOVER = 1
        PRESSED = 2

    class EventTypes:
        """Game button events."""
        CLICK = 'CLICK'
        HOVER = 'HOVER'
        LEAVE = 'LEAVE'
        PRESS = 'PRESS'

    def __init__(
        self,
        rect,
        text,
        on_click=lambda *args, **kwargs: None,
        padding=5,
        font=None,
    ):
        """Initialize button.

        Args:
            rect (pygame.Rect): Button rect.
            text (string): Button caption.
            on_click (function, optional): Button on_click event. Defaults to lambda*args.
            padding (int, optional): Padding for button text. Defaults to 5.
            font (Font, optional): Font for button text. Defaults to None.
        """
        super().__init__()
        self.image = pygame.Surface((rect.width, rect.height))
        self.rect = rect

        self.__text = text
        self.on_click = on_click

        self.text = TextObject(
            x=padding,
            y=padding,
            text=self.caption,
            font=font,
        )

        self.state = self.States.NORMAL
        self.events = Events({
            pygame.MOUSEMOTION: self.on_mouse_move,
            pygame.MOUSEBUTTONDOWN: self.on_mouse_down,
            pygame.MOUSEBUTTONUP: self.on_mouse_up,
        })

    @property
    def is_hovered(self):
        """Get if button is hovered.

        Returns:
            bool: Button is hovered.
        """
        return self.state == self.States.HOVER

    @is_hovered.setter
    def is_hovered(self, value):
        """Set button is hovered.

        Args:
            value (bool): Button is hovered.
        """
        if value:
            self.state = self.States.HOVER
        else:
            self.state = self.States.NORMAL

    @property
    def is_pressed(self):
        """Get if button is pressed.

        Returns:
            bool: Button is pressed.
        """
        return self.state == self.States.PRESSED

    @is_pressed.setter
    def is_pressed(self, value):
        """Set button is pressed.

        Args:
            value (bool): Button is pressed.
        """
        if value:
            self.state = self.States.PRESSED
        else:
            self.state = self.States.HOVER

    def caption(self):
        """Get button caption,

        Returns:
            string: Button caption.
        """
        return self.__text

    def __draw_background(self):
        """Draw button background."""
        if self.state == self.States.NORMAL:
            self.image.fill((255, 255, 255))
        elif self.state == self.States.HOVER:
            self.image.fill((0, 255, 255))
        elif self.state == self.States.PRESSED:
            self.image.fill((0, 0, 255))

    def update(self, *args, **kwargs):
        """Redraw button."""
        self.__draw_background()
        self.text.draw(self.image)

    # Events

    def click(self, *args, **kwargs):
        """Button click action."""
        self.on_click(*args, **kwargs)
        self.hover(*args, **kwargs)

    def hover(self, *args, **kwargs):
        """Button hover action."""
        self.is_hovered = True

    def leave(self, *args, **kwargs):
        """Button leave action."""
        self.is_hovered = False

    def press(self, *args, **kwargs):
        """Button press action."""
        self.is_pressed = True

    # Handlers

    def on_mouse_move(self, *args, event=None, **kwargs):
        """On mouse move.

        Args:
            event (pygame.Event, optional): Event data. Defaults to None.
        """
        if not event:
            return

        if not self.rect.collidepoint(event.pos):
            self.leave(*args, **kwargs)
            return

        if self.state == self.States.PRESSED:
            return

        self.hover(*args, **kwargs)

    def on_mouse_down(self, *args, event=None, **kwargs):
        """On mouse button down.

        Args:
            event (pygame.Event, optional): Event data. Defaults to None.
        """
        if not event:
            return

        if not self.rect.collidepoint(event.pos):
            return

        self.press(*args, **kwargs)

    def on_mouse_up(self, *args, **kwargs):
        """On mouse button up."""
        if self.state != self.States.PRESSED:
            return

        self.click(*args, **kwargs)
