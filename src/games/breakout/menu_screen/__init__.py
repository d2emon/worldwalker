from windows.screen import Screen
from .groups.menu_items import BreakoutMenuItems


class MenuScreen(Screen):
    def __init__(self, size, sprites=()):
        super().__init__(size)

        for sprite in sprites:
            self.sprites.add(sprite)

        self.menu_items = BreakoutMenuItems()
        self.menu_items.events.listeners.append(self.events)

    def update(self):
        super().update()
        self.menu_items.update()

    def draw(self):
        super().draw()
        self.menu_items.draw(self)
