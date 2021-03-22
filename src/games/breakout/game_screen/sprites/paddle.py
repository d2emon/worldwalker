import pygame
from windows.controls.moving import Moving
from games.breakout.intersect import intersect
from games.breakout.game_screen.sprites.ball import Ball


class Paddle(Moving):
    class States:
        STAND = 0
        RIGHT = 1
        LEFT = -1

    def __init__(
        self,
        pos=None,
        base_speed=10,
    ):
        super().__init__(pygame.Rect(300, 400, 80, 20), (0, 0))
        self.image = self.draw()
        self.rect.center = pos or self.rect.center

        self.state = self.States.STAND
        self.ball = None
        self.__base_speed = base_speed

        self.lives = 5
        self.score = 0

    @property
    def has_started(self):
        return self.ball is not None

    @property
    def game_over(self):
        return self.lives <= 0

    @classmethod
    def draw(cls):
        image = pygame.Surface((80, 20), pygame.SRCALPHA)
        image.fill((255, 0, 0))
        return image

    @property
    def speed(self):
        if self.state == self.States.LEFT:
            return -self.__base_speed, 0
        elif self.state == self.States.RIGHT:
            return self.__base_speed, 0
        else:
            return 0, 0

    def move_left(self):
        self.state = self.States.LEFT

    def move_right(self):
        self.state = self.States.RIGHT

    def stop(self):
        self.state = self.States.STAND

    def start(self, pos):
        self.ball = Ball(*pos)

    def loose(self):
        # self.sound_effects['paddle_hit'].play()
        self.lives -= 1
        self.ball = None

    def update(self, *args):
        super().update(*args)

        if self.ball is None:
            return

        if self.ball.fallen:
            return self.loose()

        edge = intersect(self.ball.rect, self.rect)
        if edge is not None:
            # self.sound_effects['paddle_hit'].play()
            self.ball.hit_paddle(edge, self.speed)
