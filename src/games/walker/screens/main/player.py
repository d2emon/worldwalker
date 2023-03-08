"""Player sprite.

Typical usage example:

  player = Player((0, 0))
"""

import pygame
from ... import resource


class Player(pygame.sprite.Sprite):
    """Player sprite.

    Attributes:
        image (pygame.Surface): Sprite image.
        rect (pygame.Rect): Sprite rect.
        speed (float): Rect speed.
        x_vel (int): Rect horyzontal speed.
        y_vel (int): Rect vertical speed.
    """
    speed = 10

    def __init__(
        self,
        screen_pos=(500, 500),
        starting_pos=(500, 500),
        field_size=(1000, 1000),
        zoom_size=(100, 100),
        level=None,
    ):
        """Initialize sprite.

        Args
            screen_pos (tuple, optional): Starting position on scren. Defaults to (500, 500).
            starting_pos (tuple, optional): Starting position. Defaults to (500, 500).
            field_size (tuple, optional): Field size. Defaults to (1000, 1000).
        """
        super().__init__()

        self.image = pygame.Surface((512, 512), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        center = 256, 256

        self.rect.center = screen_pos
        self.__field_size = field_size
        self.__starting_pos = starting_pos
        self.pos = [*starting_pos]
        self.zoom_size = zoom_size

        self.level = level

        zoom_rect = pygame.Rect((0, 0), zoom_size)
        zoom_rect.center = center
        pygame.draw.rect(self.image, (255, 255, 255, 4), zoom_rect)
        pygame.draw.ellipse(self.image, (0, 0, 255, 32), zoom_rect)

        image = resource.player_image()
        image_rect = image.get_rect()
        image_rect.center = center
        self.image.blit(resource.player_image(), image_rect)

    @property
    def field_size(self):
        if self.level:
            return self.level.size
        else:
            return self.__field_size

    @property
    def starting_pos(self):
        if self.level:
            return self.level.starting_pos
        else:
            return self.__starting_pos

    def __check_constraints(self):
        for coord, value in enumerate(self.pos):
            if value < 0:
                self.pos[coord] = 0
            if value > self.field_size[coord]:
                self.pos[coord] = self.field_size[coord]

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
