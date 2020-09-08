import pygame
import config
from pygame.sprite import Sprite


class MapSprite(Sprite):
    def __init__(self, rect):
        super().__init__()
        self.__map_image = self.__load_map()

        self.image = pygame.Surface((rect.width, rect.height))
        self.rect = pygame.Rect(rect)

        self.viewpoint = pygame.Rect(rect)
        self.viewpoint.center = config.VIEWPOINT

    @classmethod
    def __load_map(cls):
        image = pygame.image.load(config.MAP_FILE)
        image = pygame.transform.scale(
            image,
            (
                int(image.get_width() * config.MAP_SCALE),
                int(image.get_height() * config.MAP_SCALE),
            ),
        )
        min_x = 210
        min_y = 185
        max_x = image.get_width() - 200
        max_y = image.get_height() - 300
        for x in range(min_x, max_x, config.SCALE):
            pygame.draw.line(image, (0, 0, 0), (x, min_y), (x, max_y))
        for y in range(min_y, max_y, config.SCALE):
            pygame.draw.line(image, (0, 0, 0), (min_x, y), (max_x, y))
        return image

    def update(self, *args):
        self.image.fill((0, 0, 0))
        self.image.blit(self.__map_image, self.rect, self.viewpoint)

    def move(self, x, y):
        scale = config.SCALE * config.TIME_SCALE
        self.viewpoint = self.viewpoint.move(x * scale, y * scale)
        print(self.viewpoint.center)
