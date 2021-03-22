import pygame
from events import Events
from .button import Button


class MenuItems(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.events = Events()

    def new_item(self, title, on_click=lambda *args, **kwargs: None):
        return Button(
            pygame.Rect(),
            title,
            on_click,
        )

    def add_item(self, title, on_click=lambda *args, **kwargs: None):
        item = self.new_item(title, on_click)
        item.events.listeners.append(self.events)
        return self.add(item)

    def emit(self, event_type, *args, event=None, **kwargs):
        for item in self:
            item.events.emit(event_type, *args, **kwargs, pos=event.pos if event else None)
