import pygame
import time


class TextObject:
    class Font:
        def __init__(self, name='Arial', size=10, color=(0, 0, 0)):
            self.name = name
            self.size = size
            self.color = color

    def __init__(self, x, y, text, font=None):
        self.pos = x, y
        self.text_func = text
        self.__font = font or self.Font()
        self.color = self.__font.color
        self.font = pygame.font.SysFont(self.__font.name, self.__font.size)
        self.bounds = self.get_surface(self.text_func())

    def update(self):
        pass

    def draw(self, surface, center=False):
        text_surface, self.bounds = self.get_surface(self.text_func())

        if center:
            pos = (self.pos[0] - self.bounds.width // 2, self.pos[1])
        else:
            pos = self.pos

        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

    @classmethod
    def show_message(
        cls,
        surface,
        text,
        font=None,
        center=False,
        duration=5,
    ):
        surface.update()
        surface.draw()

        rect = surface.get_rect()
        message = TextObject(
            rect.centerx,
            rect.centery,
            lambda: text,
            font or cls.Font(
                name='Arial',
                size=20,
                color=(255, 255, 255),
            ),
        )
        message.draw(surface, center)

        pygame.display.update()
        time.sleep(duration)
