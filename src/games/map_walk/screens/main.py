import pygame
from pygame.sprite import LayeredUpdates
from games.map_walk.sprites.map import MapSprite
from games.map_walk.sprites.player import Player
from windows.windows.window import Window


class Sprites(LayeredUpdates):
    def __init__(self, rect):
        super().__init__()

        self.map_sprite = MapSprite(rect)
        self.player = Player(rect.center)

        self.add(self.map_sprite, layer=0)
        self.add(self.player, layer=1)


class MainScreen(pygame.Surface):
    def __init__(self, rect):
        super().__init__((rect.width, rect.height))

        self.sprites = Sprites(rect)

        self.events = {
            Window.UPDATE: self.__on_update,
            Window.KEYDOWN: self.__on_key_down,
        }

    @property
    def player(self):
        return self.sprites.player

    @property
    def map_sprite(self):
        return self.sprites.map_sprite

    def __on_update(self, *args, **kwargs):
        self.sprites.update()
        self.sprites.draw(self)

    def __on_key_down(self, *args, keys=None, **kwargs):
        speed = self.player.speed
        if keys[pygame.K_LEFT]:
            self.map_sprite.move(-speed, 0)
        if keys[pygame.K_RIGHT]:
            self.map_sprite.move(speed, 0)
        if keys[pygame.K_UP]:
            self.map_sprite.move(0, -speed)
        if keys[pygame.K_DOWN]:
            self.map_sprite.move(0, speed)
