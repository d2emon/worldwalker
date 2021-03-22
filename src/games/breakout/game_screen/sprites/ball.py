import pygame
from windows.controls.moving import Moving
from games.breakout.intersect import get_bounds, COLLIDE_LEFT, COLLIDE_TOP, COLLIDE_RIGHT, COLLIDE_BOTTOM, COLLIDE_HORIZONTAL, COLLIDE_VERTICAL


class Ball(Moving):
    def __init__(
        self,
        pos=None,
        speed=(0, 1),
    ):
        super().__init__(pygame.Rect(0, 0, 10, 10), speed)
        self.image = self.draw()
        self.rect.center = pos or self.rect.center
        self.fallen = False

    @classmethod
    def draw(cls):
        color = (0, 255, 0)
        r = 5

        image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(image, color, image.get_rect().center, r)
        return image

    def reverse_x(self):
        x, y = self.speed
        self.speed = -x, y

    def reverse_y(self):
        x, y = self.speed
        self.speed = x, -y

    def update_speed(self, speed):
        x, y = self.speed
        dx, dy = speed
        self.speed = (x + dx), -(y + dy)

    def hit_paddle(self, edge, speed):
        if edge in COLLIDE_HORIZONTAL:
            self.reverse_x()
        elif edge in COLLIDE_VERTICAL:
            self.update_speed(speed)

    def hit_brick(self, edge):
        if edge in COLLIDE_HORIZONTAL:
            # self.sound_effects['paddle_hit'].play()
            self.reverse_x()
        elif edge in COLLIDE_VERTICAL:
            # self.sound_effects['paddle_hit'].play()
            self.reverse_y()

    def update(self, bounds, *args):
        super().update(*args)

        for edge in get_bounds(self.rect, bounds):
            if edge == COLLIDE_BOTTOM:
                self.fallen = True
            else:
                self.hit_brick(edge)
