import pygame
from config.games import breakout as config
from events import Events
from windows.controls import Button, MenuItems, TextObject
from ... import events


class BreakoutMenuItems(MenuItems):
    def __init__(self, on_click):
        super().__init__()

        self.font = TextObject.Font(
            config.BUTTON_FONT_NAME,
            config.BUTTON_FONT_SIZE,
            config.BUTTON_FONT_COLOR,
        )

        self.__rect = pygame.Rect(
            config.BUTTON_MARGIN[0],
            config.BUTTON_MARGIN[1],
            config.BUTTON_WIDTH,
            config.BUTTON_HEIGHT,
        )

        on_emit = lambda event_type, *args, **kwargs : print("BREAKOUT MENU ITEMS", event_type, args, kwargs)
        self.events = Events({
            events.MOUSE_BUTTON_DOWN: self.emit,
            events.MOUSE_BUTTON_UP: self.emit,
            events.MOUSE_MOTION: self.emit,
        }, on_emit)

        self.__on_item_click = on_click

        self.add_item('PLAY', self.on_select(events.MENU_PLAY))
        self.add_item('QUIT', self.on_select(events.MENU_QUIT))

    @property
    def item_width(self):
        return self.__rect.width + config.BUTTON_MARGIN[0] * 2

    @property
    def item_height(self):
        return self.__rect.height + config.BUTTON_MARGIN[1] * 2

    def get_rect(self):
        return self.__rect.move(
            0,
            len(self) * self.item_height,
        )

    def new_item(self, title, on_click=lambda *args, **kwargs: None):
        return Button(
            self.get_rect(),
            title,
            on_click,
            font=self.font,
            padding=config.BUTTON_PADDING,
        )

    def on_select(self, event_id):
        # return lambda *args, **kwargs: self.events.emit(event_id, *args, **kwargs)
        def f(*args, **kwargs):
            print("SELECT", event_id, args, kwargs)
            self.events.emit(event_id, *args, **kwargs)
            self.__on_item_click(event_id, *args, **kwargs)
        
        return f
