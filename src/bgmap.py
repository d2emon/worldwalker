import resources
from pygame import image, sprite


MOVE_SPEED = 32
WIDTH = 800
HEIGHT = 600
CONSTS = ((-1600, 1600), (-1200, 1200))


class BgMap(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.startX = x
        self.startY = y
        self.x = self.startX
        self.y = self.startY
        self.image = image.load(resources.MAPFILE)
        self.rect = self.image.get_rect()
        self.moveTo(self.x, self.y)

    def update(self, xvel, yvel):
        self.xvel = xvel * MOVE_SPEED
        self.yvel = yvel * MOVE_SPEED
        if (xvel == 0) and (yvel == 0):
            self.xvel = 0
            self.yvel = 0
        self.x += self.xvel
        self.y += self.yvel
        self.moveTo(self.x, self.y)

    def moveTo(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.testBounds()

    def testBounds(self):
        if self.x <= CONSTS[0][0]:
            self.x = CONSTS[0][0] + 32
        if self.x >= CONSTS[0][1]:
            self.x = CONSTS[0][1] - 32
        if self.y <= CONSTS[1][0]:
            self.y = CONSTS[1][0] + 32
        if self.y >= CONSTS[1][1]:
            self.y = CONSTS[1][1] - 32

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
