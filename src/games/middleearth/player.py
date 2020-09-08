from . import resources
from pygame import image
from pygame.sprite import DirtySprite


MOVE_SPEED = 7
WIDTH = 32
HEIGHT = 32
CONSTS = ((10, 758), (10, 588))


class Player(DirtySprite):
    def __init__(self, x, y):
        self._layer = 3
        super().__init__()
        self.speed = 0, 0
        self.start_pos = x, y

        self.image = image.load(resources.FLYFILE)
        self.rect = self.image.get_rect()
        self.moveTo(*self.start_pos)

    def set_speed(self, speed):
        dx, dy = speed
        self.speed = (
            dx * MOVE_SPEED,
            dy * MOVE_SPEED,
        )
        if (dx == 0) and (dy == 0):
            self.speed = 0, 0

    def update(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.x <= CONSTS[0][0]:
            self.rect.x = CONSTS[0][0] + 1
        if self.rect.x >= CONSTS[0][1]:
            self.rect.x = CONSTS[0][1] - 1
        if self.rect.y <= CONSTS[1][0]:
            self.rect.y = CONSTS[1][0] + 1
        if self.rect.y >= CONSTS[1][1]:
            self.rect.y = CONSTS[1][1] - 1

    def moveTo(self, x, y):
        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height / 2
