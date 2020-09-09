from pygame.sprite import Sprite


class Moving(Sprite):
    def __init__(self, rect=None, speed=(0, 0)):
        super().__init__()
        self.rect = rect
        self.__speed = speed

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        self.__speed = value

    def update(self, *args):
        self.rect = self.rect.move(*self.speed)
