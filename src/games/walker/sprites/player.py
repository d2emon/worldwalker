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
    speed = 10

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

        self.starting_pos = starting_pos
        self.pos = [*starting_pos]

    def __check_constraints(self):
        for coord, value in enumerate(self.pos):
            if value < 0:
                self.pos[coord] = 0
            if value > 1000:
                self.pos[coord] = 1000

        return [*self.pos]

    def move_by(self, x_vel, y_vel):
        """Move sprite viewpoint.

        Args:
            x_vel (float): Moves by x.
            y_vel (float): Moves by y.

        Returns:
            list: Player position.
        
        """
        self.pos[0] += x_vel * self.speed
        self.pos[1] += y_vel * self.speed
        return self.__check_constraints()

    def reset_viewpoint(self):
        """Reset player position.

        Returns:
            list: Player position.
        """
        self.pos = [*self.starting_pos]
        return self.__check_constraints()
