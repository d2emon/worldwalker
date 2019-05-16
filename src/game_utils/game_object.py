from pygame.rect import Rect
from pygame.sprite import Sprite


class GameObject(Sprite):
    def __init__(self, x, y, w, h, speed=(0, 0)):
        super().__init__()
        self.rect = Rect(x, y, w, h)
        self.speed = speed

    @property
    def left(self):
        return self.rect.left

    @property
    def right(self):
        return self.rect.right

    @property
    def top(self):
        return self.rect.top

    @property
    def bottom(self):
        return self.rect.bottom

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    @property
    def center(self):
        return self.rect.center

    @property
    def centerx(self):
        return self.rect.centerx

    @property
    def centery(self):
        return self.rect.centery

    def draw(self, surface):
        raise NotImplementedError()

    def move(self, dx, dy):
        self.rect = self.rect.move(dx, dy)

    def update(self):
        if self.speed == [0, 0]:
            return

        self.rect.move(*self.speed)
