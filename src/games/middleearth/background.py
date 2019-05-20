from . import resources
from pygame import image
from pygame.sprite import DirtySprite


class Background(DirtySprite):
    def __init__(self):
        super().__init__()
        self.image = image.load(resources.BGFILE)
        self.rect = self.image.get_rect()
