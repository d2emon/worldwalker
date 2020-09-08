import pygame
import config
from pygame.sprite import Sprite
from games.map_walk.red_earth import PLAYER_SPEED


class Player(Sprite):
    __COLOR = (0, 255, 0)

    def __init__(self, center=(0, 0)):
        super().__init__()
        self.image = self.__draw_player()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = PLAYER_SPEED

    @classmethod
    def __draw_player(cls):
        width = height = config.PLAYER_VIEW * 2
        image = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        rect = image.get_rect()
        pygame.draw.circle(image, config.PLAYER_VIEW_COLOR, rect.center, config.PLAYER_VIEW, 2)
        pygame.draw.circle(image, config.PLAYER_COLOR, rect.center, config.PLAYER_SIZE)
        return image
