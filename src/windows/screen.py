import pygame
from pygame import image
from pygame.sprite import Group
from events import Events


class Screen(pygame.Surface):
    BACKGROUND_IMAGE = "../res/global/map.jpg"
    BACKGROUND_POS = 0, 0
    background = None

    def __init__(self, size):
        super().__init__(size)

        self.image = self.load_image()
        self.pos = self.BACKGROUND_POS
        self.sprites = Group()
        self.events = Events()

    def load_image(self):
        return pygame.image.load(self.BACKGROUND_IMAGE)

    def update(self, *args):
        self.sprites.update(*args)

    def draw(self):
        self.blit(self.image, self.pos)
        self.sprites.draw(self)
