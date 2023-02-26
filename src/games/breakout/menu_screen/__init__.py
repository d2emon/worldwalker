from windows.screen import Screen
from .groups.menu_items import BreakoutMenuItems


class MenuScreen(Screen):
    def __init__(self, size, sprites=()):
        super().__init__(size)

        for sprite in sprites:
            self.sprites.add(sprite)

        self.menu_items = BreakoutMenuItems(self.on_item_click)
        self.events.listeners.append(self.menu_items)

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.menu_items.update(*args, **kwargs)

    def draw(self):
        super().draw()
        self.menu_items.draw(self)

    def on_item_click(self, *args, **kwargs):
        print("ITEM CLICK", args, kwargs)
