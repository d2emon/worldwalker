"""Game menu.

Typical usage example:

  menu = MenuItems()
  menu.add_item("Button 1", on_click)
  menu.add_item("Button 2", on_click)
"""

import pygame
from events import Events
from .button import Button


class MenuItems(pygame.sprite.Group):
    """Game menu sprite.

    Attributes:
        events (Events): Menu events.
    """

    def __init__(self):
        """Initialize game menu."""
        super().__init__()
        self.events = Events()

    @classmethod
    def new_item(cls, title, on_click=lambda *args, **kwargs: None):
        """Create menu item.

        Args:
            title (string): Menu item caption.
            on_click (function, optional): Menu item on click event. Defaults to lambda*args.

        Returns:
            Button: New item for menu.
        """
        return Button(
            pygame.Rect(),
            title,
            on_click,
        )

    def add_item(self, title, on_click=lambda *args, **kwargs: None):
        """Add menu item.

        Args:
            title (string): Menu item caption.
            on_click (function, optional): Menu item on click event. Defaults to lambda*args.
        """
        item = self.new_item(title, on_click)
        return self.add(item)

    def emit(self, event_type, *args, **kwargs):
        """Emit event in all manu items.

        Args:
            event_type (int): Event type.
        """
        for item in self:
            item.events.emit(event_type, *args, **kwargs)
