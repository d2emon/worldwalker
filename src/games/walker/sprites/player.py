"""Player sprite.

Typical usage example:

  player = Player((0, 0))
"""

import pygame
import config


class Player(pygame.sprite.Sprite):
    """Player sprite.

    Attributes:
        image (pygame.Surface): Sprite image.
        rect (pygame.Rect): Sprite rect.
        speed (float): Rect speed.
        x_vel (int): Rect horyzontal speed.
        y_vel (int): Rect vertical speed.
    """

    __filename = config.Universe.PLAYER
    __speed = 10

    def __init__(self, rect, starting_pos=(500, 500)):
        """Initialize sprite.

        Args
            rect (pygame.Rect): Screen rect.
            starting_pos (tuple, optional): Starting position. Defaults to (500, 500).
        """
        super().__init__()
        self.image = pygame.image.load(self.__filename)
        self.rect = self.image.get_rect()
        self.rect.center = rect.center

        self.speed = self.__speed
        self.x_vel = self.y_vel = 0
        self.starting_pos = starting_pos
        self.pos = [*starting_pos]

    def __check_constraints(self):
        for coord, value in enumerate(self.pos):
            if value < 0:
                self.pos[coord] = 0
            if value > 1000:
                self.pos[coord] = 1000

    def move_viewpoint(self, x, y):
        """Move sprite viewpoint.

        Args:
            x (float): Moves by x.
            y (float): Moves by y.
        """
        self.pos[0] += x * self.speed
        self.pos[1] += y * self.speed
        self.__check_constraints()

    def move(self):
        """Move sprite."""
        self.move_viewpoint(self.x_vel, self.y_vel)

    def reset_viewpoint(self, *args, **kwargs):
        """Reset player position."""
        self.pos = [*self.starting_pos]
        self.__check_constraints()
