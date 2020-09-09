import pygame
from windows.controls.moving import Moving


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

        self.lives = 5
        self.score = 0
        self.state = self.States.STAND
        self.__base_speed = base_speed

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
