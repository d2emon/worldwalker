import random
import pygame
from pygame import draw, Rect, Surface
from pygame.sprite import Sprite
from game_utils import Button


class MenuItem(Button):
    OFFSET_X = 5
    OFFSET_Y = 5
    BUTTON_W = 200
    BUTTON_H = 20

    def __init__(self, item_id, text, handler):
        super().__init__(
            Rect(
                self.OFFSET_X,
                self.OFFSET_Y + (self.BUTTON_H + 5) * item_id,
                self.BUTTON_W,
                self.BUTTON_H,
            ),
            text,
            handler,
            padding=5,
        )


class Paddle(Sprite):
    START_X = 300
    START_Y = 400
    WIDTH = 80
    HEIGHT = 20
    COLOR = 255, 0, 0
    SPEED = 10

    def __init__(self, field):
        super().__init__()
        self.color = self.COLOR
        self.speed = self.SPEED
        self.field = field
        self.moving_left = False
        self.moving_right = False

        self.rect = Rect(
            self.START_X,
            self.START_Y,
            self.WIDTH,
            self.HEIGHT,
        )
        self.image = Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.color)

    def update(self):
        if self.moving_left:
            dx = -min(self.speed, self.rect.left)
        elif self.moving_right:
            dx = min(self.speed, self.field.right - self.rect.right)
        else:
            return

        self.rect = self.rect.move(dx, 0)

    def handle(self, event):
        if event.key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
        elif event.key == pygame.K_RIGHT:
            self.moving_right = not self.moving_right


class Ball(Sprite):
    BALL_SPEED = 1
    BALL_RADIUS = 5
    BALL_COLOR = 0, 255, 0

    def __init__(self, x, y):
        super().__init__()
        self.radius = self.BALL_RADIUS
        self.color = self.BALL_COLOR
        self.speed = random.randint(-2, 2), self.BALL_SPEED

        self.rect = Rect(
            x - self.radius,
            y - self.radius,
            self.diameter,
            self.diameter
        )
        self.image = Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

    @property
    def diameter(self):
        return self.radius * 2

    def update(self, *args):
        self.rect = self.rect.move(*self.speed)

    def intersect(self, obj_rect):
        edges = dict(
            left=Rect(obj_rect.left, obj_rect.top, 1, obj_rect.height),
            right=Rect(obj_rect.right, obj_rect.top, 1, obj_rect.height),
            top=Rect(obj_rect.left, obj_rect.top, obj_rect.width, 1),
            bottom=Rect(obj_rect.left, obj_rect.bottom, obj_rect.width, 1),
        )
        collisions = set(edge for edge, rect in edges.items() if self.rect.colliderect(rect))

        if not collisions:
            return None

        if len(collisions) == 1:
            return list(collisions)[0]

        if 'top' in collisions:
            if self.rect.centery >= obj_rect.top:
                return 'top'
            elif self.rect.centerx >= obj_rect.left:
                return 'left'
            else:
                return 'right'

        if 'bottom' in collisions:
            if self.rect.centery >= obj_rect.bottom:
                return 'bottom'
            elif self.rect.centerx < obj_rect.left:
                return 'left'
            else:
                return 'right'


class Brick(Sprite):
    BRICK_WIDTH = 80
    BRICK_HEIGHT = 20
    BRICK_COLOR = 0, 0, 255

    def __init__(self, x, y, effect=None):
        super().__init__()
        self.color = self.BRICK_COLOR
        self.effect = effect

        self.rect = Rect(
            x * (self.BRICK_WIDTH + 1),
            y * (self.BRICK_HEIGHT + 1),
            self.BRICK_WIDTH,
            self.BRICK_HEIGHT,
        )
        self.image = Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)
