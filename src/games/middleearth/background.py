from games.middleearth import resources
from pygame import Surface, image


class Background(Surface):
    def __init__(self, size):
        Surface.__init__(self, size)
        self.image = image.load(resources.BGFILE)
        self.blit(self.image, (0, 0))

    def draw(self, screen):
        screen.blit(self, (0, 0))
