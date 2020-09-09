import pygame
from .sprite import BreakoutSprite


class Paddle(BreakoutSprite):
    class States:
        STAND = 0
        RIGHT = 1
        LEFT = -1

    def __init__(
        self,
        rect=None,
        pos=None,
        color=None,
        speed=10,
    ):
        self.color = color or (255, 0, 0)
        super().__init__(
            rect or pygame.Rect(300, 400, 80, 20),
            pos,
        )

        self.lives = 5
        self.score = 0
        self.state = self.States.STAND
        self.__base_speed= speed

    def draw(self):
        image = pygame.Surface((self.rect.width, self.rect.height))
        image.fill(self.color)
        return image

    @property
    def speed(self):
        if self.state == self.States.LEFT:
            return -self.__base_speed, 0
        elif self.state == self.States.RIGHT:
            return self.__base_speed, 0
        else:
            return 0, 0

    @property
    def game_over(self):
        return self.lives <= 0

    def move_left(self):
        self.state = self.States.LEFT

    def move_right(self):
        self.state = self.States.RIGHT

    def stop(self):
        self.state = self.States.STAND

    def loose(self):
        self.lives -= 1
