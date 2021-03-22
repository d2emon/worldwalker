import pygame
from config.games import breakout as config
from games.breakout.intersect import intersect
from games.breakout.sprites import Brick


class Bricks(pygame.sprite.Group):
    def __init__(self):
        super().__init__([
            self.__brick((x, y))
            for x in range(config.BUTTON_WIDTH)
            for y in range(config.BRICKS_HEIGHT)
        ])

    @classmethod
    def __brick(cls, pos=(0, 0)):
        return Brick((
            10 + pos[0] * (40 + 1),
            10 + pos[1] * (10 + 1),
        ))

    def update(self, player, *args):
        if not player.has_started:
            return

        for brick in self:
            edge = intersect(player.ball.rect, brick.rect)

            if not edge:
                continue

            player.ball.hit_brick(edge)
            player.score += brick.points
            self.remove(brick)

        super().update(*args)
