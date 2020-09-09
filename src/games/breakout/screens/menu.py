import pygame
from pygame.sprite import Group
from windows.screen import Screen
from windows.controls import Button, TextObject


class MenuScreen(Screen):
    def __init__(self, size, menu_items=()):
        super().__init__(size)

        for menu_item in menu_items:
            self.sprites.add(menu_item)

        self.button_rect = pygame.Rect(5, 5, 250, 50)
        self.font = TextObject.Font(
            'Arial',
            20,
            (0, 0, 0),
        )

        self.events.events[pygame.MOUSEBUTTONDOWN] = self.button_event
        self.events.events[pygame.MOUSEBUTTONUP] = self.button_event
        self.events.events[pygame.MOUSEMOTION] = self.button_event

    def add_menu_item(self, title, on_click=lambda *args, **kwargs: None):
        self.sprites.add(Button(
            self.button_rect.move(
                0,
                len(self.sprites) * (5 + self.button_rect.height + 5),
            ),
            title,
            on_click,
            font=self.font,
            padding=5,
        ))

    def button_event(self, event_type, *args, event=None, **kwargs):
        for button in self.sprites:
            button.events.emit(event_type, *args, **kwargs, pos=event.pos if event else None)
