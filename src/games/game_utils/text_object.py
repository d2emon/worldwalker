import pygame


class Font:
    def __init__(self, name='Arial', size=10, color=(0, 0, 0)):
        self.name = name
        self.size = size
        self.color = color


class TextObject:
    def __init__(self, x, y, text_func, font):
        self.pos = x, y
        self.text_func = text_func
        self.color = font.color
        self.font = pygame.font.SysFont(font.name, font.size)
        self.bounds = self.get_surface(text_func())

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
