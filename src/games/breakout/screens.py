import time
import pygame
from pygame import image, Surface
from pygame.sprite import Group
from games.game_utils import Font, TextObject
from .sprites import MenuItem, Paddle, Brick, Ball


class BaseScreen(Surface):
    MESSAGE_DURATION = 5

    BACKGROUND_IMAGE = "../res/global/map.jpg"
    BACKGROUND_POS = 0, 0
    background = None

    def __init__(self, size):
        super().__init__(size)
        if self.background is None:
            self.background = image.load(self.BACKGROUND_IMAGE)
        self.background_pos = self.BACKGROUND_POS
        self.sprites = Group()

        self.event_handlers = dict()

    def update(self):
        self.sprites.update()
        self.blit(self.background, self.background_pos)
        self.sprites.draw(self)

    def show_message(
        self,
        text,
        color=(255, 255, 255),
        font_name='Arial',
        font_size=20,
        center=False,
    ):
        rect = self.get_rect()
        message = TextObject(
            rect.centerx,
            rect.centery,
            lambda: text,
            Font(
                font_name,
                font_size,
                color,
            ),
        )
        self.update()
        message.draw(self, center)
        pygame.display.update()
        time.sleep(self.MESSAGE_DURATION)


class MenuScreen(BaseScreen):
    def __init__(self, size, menu_items):
        super().__init__(size)

        self.mouse_handlers = []
        for item_id, (text, handler) in enumerate(menu_items):
            button = MenuItem(item_id, text, handler)
            self.sprites.add(button)
            self.mouse_handlers.append(button.handle_mouse_event)
        self.event_handlers = {
            pygame.MOUSEBUTTONDOWN: self.mouse_handlers,
            pygame.MOUSEBUTTONUP: self.mouse_handlers,
            pygame.MOUSEMOTION: self.mouse_handlers,
        }


class GameScreen(BaseScreen):
    EVENT_WIN = 100
    EVENT_LOOSE = 200

    def __init__(self, size, events=None):
        super().__init__(size)
        self.game_rect = self.get_rect()

        self.lives = 5
        self.score = 0
        self.points_per_brick = 10

        self.events = events or dict()

        self.paddle = Paddle(self.game_rect)
        self.bricks = Group([
            Brick(i, j)
            for i in range(10)
            for j in range(5)
        ])
        self.ball = None

        self.sprites.add(self.paddle, *self.bricks)
        self.create_ball()

        self.event_handlers = {
            pygame.KEYDOWN: [self.paddle.handle],
            pygame.KEYUP: [self.paddle.handle],
        }

    def create_ball(self):
        self.ball = Ball(self.game_rect.centerx, self.game_rect.centery)
        self.sprites.add(self.ball)

    def update(self):
        super().update()

        speed = self.ball.speed
        paddle_edge = self.ball.intersect(self.paddle.rect)
        # if paddle_edge is not None:
        #     self.sound_effects['paddle_hit'].play()

        if paddle_edge == 'top':
            speed_x = speed[0]
            speed_y = -speed[1]
            if self.paddle.moving_left:
                speed_x -= 1
            elif self.paddle.moving_right:
                speed_x += 1
            self.ball.speed = speed_x, speed_y
        elif paddle_edge in ('left', 'right'):
            self.ball.speed = -speed[0], speed[1]

        # If ball gets off the screen
        if self.ball.rect.bottom > self.game_rect.bottom:
            self.lives -= 1
            if self.lives <= 0:
                return self.loose_game()
            else:
                self.create_ball()
        if self.ball.rect.top < self.game_rect.top:
            self.ball.speed = speed[0], -speed[1]
        if self.ball.rect.left < self.game_rect.left or self.ball.rect.right >= self.game_rect.right:
            self.ball.speed = -speed[0], speed[1]

        if not self.bricks:
            return self.win_game()

        for brick in self.bricks:
            brick_edge = self.ball.intersect(brick.rect)
            if not brick_edge:
                continue

            self.bricks.remove(brick)
            self.sprites.remove(brick)
            self.score += self.points_per_brick

            if brick_edge in ('top', 'bottom'):
                self.ball.speed = speed[0], -speed[1]
            else:
                self.ball.speed = -speed[0], speed[1]

    def handle_event(self, event_type):
        event = self.events.get(event_type)
        if event is None:
            return
        return event()

    def win_game(self):
        self.show_message("YOU WIN!!!", center=True)
        return self.handle_event(self.EVENT_WIN)

    def loose_game(self):
        return self.handle_event(self.EVENT_LOOSE)
