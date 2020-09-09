import pygame
from windows.windows import Window
from windows.screen import Screen
from windows.controls import TextObject
from ..intersect import intersect, COLLIDE_TOP, COLLIDE_BOTTOM, COLLIDE_LEFT, COLLIDE_RIGHT
from ..sprites import Paddle, Brick, Ball


class GameScreen(Screen):
    EVENT_START = 100
    EVENT_WIN = 200
    EVENT_LOOSE = 300

    def __init__(self, size):
        super().__init__(size)
        self.rect = self.get_rect()

        self.paddle = self.add_paddle((self.rect.centerx, 400))
        self.bricks = pygame.sprite.Group([
            self.add_brick((x, y))
            for x in range(6)
            for y in range(4)
        ])
        self.ball = None

        self.events.events[self.EVENT_START] = self.on_start
        self.events.events[Window.KEYDOWN] = self.on_key_down
        self.events.events[Window.KEYUP] = self.on_key_up

        self.events.emit(self.EVENT_START)

    def add_paddle(self, pos=(0, 0)):
        paddle = Paddle(
            pygame.Rect(0, 0, 80, 20),
            pos,
        )
        self.sprites.add(paddle)
        return paddle

    def add_brick(self, pos=(0, 0)):
        brick = Brick(
            pygame.Rect(0, 0, 80, 20).move(
                10 + pos[0] * (80 + 2),
                10 + pos[1] * (20 + 2),
            ),
            (0, 0, 255),
        )
        self.sprites.add(brick)
        return brick

    def add_ball(self, pos=(0, 0)):
        ball = Ball(
            pygame.Rect(0, 0, 10, 10),
            pos,
        )
        self.sprites.add(ball)
        return ball

    def remove_brick(self, brick):
        self.paddle.score += brick.points
        self.sprites.remove(brick)
        self.bricks.remove(brick)

    def on_start(self, *args, **kwargs):
        self.ball = self.add_ball(self.rect.center)

    def update(self):
        super().update()

        if self.ball is None:
            return

        if not self.bricks:
            return self.events.emit(self.EVENT_WIN)

        # If ball gets off the screen
        if self.ball.rect.bottom > self.rect.bottom:
            self.paddle.loose()
            return self.events.emit(self.EVENT_LOOSE if self.paddle.game_over else self.EVENT_START)

        if self.ball.rect.top < self.rect.top:
            self.ball.reverse_y()
        if self.ball.rect.left < self.rect.left or self.ball.rect.right >= self.rect.right:
            self.ball.reverse_x()

        edge = intersect(self.ball.rect, self.paddle.rect)
        if edge is not None:
            # if edge is not None:
            #     self.sound_effects['paddle_hit'].play()
            if edge in (COLLIDE_TOP, COLLIDE_BOTTOM):
                self.ball.struck(self.paddle.speed)
            else:
                self.ball.reverse_x()

        for brick in self.bricks:
            edge = intersect(self.ball.rect, brick.rect)
            if edge:
                self.remove_brick(brick)
                if edge in (COLLIDE_TOP, COLLIDE_BOTTOM):
                    self.ball.reverse_y()
                else:
                    self.ball.reverse_x()

    def on_key_down(self, *args, keys=None, **kwargs):
        if keys is None:
            return
        if self.paddle is None:
            return
        if keys[pygame.K_LEFT]:
            self.paddle.move_left()
        if keys[pygame.K_RIGHT]:
            self.paddle.move_right()

    def on_key_up(self, *args, keys=None, **kwargs):
        if keys is None:
            return
        if self.paddle is None:
            return
        self.paddle.stop()
