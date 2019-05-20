from games.middleearth import resources
from pygame import sprite, image


MOVE_SPEED = 7
WIDTH = 32
HEIGHT = 32
CONSTS = ((10, 758), (10, 588))


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.startX = x
        self.startY = y
        # self.image = Surface((WIDTH, HEIGHT))
        # self.image.fill(Color(COLOR))
        # self.rect = Rect(x, y, WIDTH, HEIGHT)
        self.image = image.load(resources.FLYFILE)
        self.rect = self.image.get_rect()
        self.moveTo(x, y)

    def update(self, xvel, yvel):
        self.xvel = xvel * MOVE_SPEED
        self.yvel = yvel * MOVE_SPEED
        if (xvel == 0) and (yvel == 0):
            self.xvel = 0
            self.yvel = 0
        self.rect.x += self.xvel
        self.rect.y += self.yvel
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

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
