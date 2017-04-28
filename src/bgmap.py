from pygame import image, sprite, Surface, Rect


MOVE_SPEED = 7
WIDTH = 800
HEIGHT = 600
CONSTS = ((10, 758), (10, 588))


class BgMap(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.startX = x
        self.startY = y
        self.image = image.load('../res/global/map.jpg')
        # self.image = Surface((WIDTH, HEIGHT))
        # self.image.blit(bg_img, (0, 0))
        self.rect = self.image.get_rect()
        # Rect(x, y, WIDTH, HEIGHT)

    def update(self, xvel, yvel):
        self.xvel = xvel * MOVE_SPEED
        self.yvel = yvel * MOVE_SPEED
        if (xvel == 0) and (yvel == 0):
            self.xvel = 0
            self.yvel = 0
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        # if self.rect.x <= CONSTS[0][0]:
        #     self.rect.x = CONSTS[0][0] + 1
        # if self.rect.x >= CONSTS[0][1]:
        #     self.rect.x = CONSTS[0][1] - 1
        # if self.rect.y <= CONSTS[1][0]:
        #     self.rect.y = CONSTS[1][0] + 1
        # if self.rect.y >= CONSTS[1][1]:
        #     self.rect.y = CONSTS[1][1] - 1

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
