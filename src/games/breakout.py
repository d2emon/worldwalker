import random
import time
import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite, Group
from game_utils import Game, Button, Font, TextObject


class MenuItem(Button):
    OFFSET_X = 5
    OFFSET_Y = 5
    BUTTON_W = 200
    BUTTON_H = 20

    def __init__(self, item_id, text, handler):
        super().__init__(
            Rect(
                self.OFFSET_X,
                self.OFFSET_Y + (self.BUTTON_H + 5) * item_id,
                self.BUTTON_W,
                self.BUTTON_H,
            ),
            text,
            handler,
            padding=5,
        )


class Paddle(Sprite):
    START_X = 300
    START_Y = 400
    WIDTH = 80
    HEIGHT = 20
    COLOR = 255, 0, 0
    SPEED = 10

    def __init__(self, field):
        super().__init__()
        self.rect = Rect(
            self.START_X,
            self.START_Y,
            self.WIDTH,
            self.HEIGHT,
        )
        self.image = pygame.Surface((self.rect.width, self.rect.height))

        self.color = self.COLOR
        self.speed = self.SPEED
        self.field = field
        self.moving_left = False
        self.moving_right = False

        self.image.fill(self.color)

    def update(self):
        if self.moving_left:
            dx = -min(self.speed, self.rect.left)
        elif self.moving_right:
            dx = min(self.speed, self.field.right - self.rect.right)
        else:
            return

        self.rect = self.rect.move(dx, 0)

    def handle(self, event):
        if event.key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
        else:
            self.moving_right = not self.moving_right


class Ball(Sprite):
    BALL_SPEED = 1
    BALL_RADIUS = 5
    BALL_COLOR = 0, 255, 0

    def __init__(self, x, y):
        super().__init__()
        self.rect = Rect(x - self.BALL_RADIUS, y - self.BALL_RADIUS, self.BALL_RADIUS * 2, self.BALL_RADIUS * 2)
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        self.radius = self.BALL_RADIUS
        self.color = self.BALL_COLOR
        self.speed = random.randint(-2, 2), self.BALL_SPEED

        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

    @property
    def diameter(self):
        return self.radius * 2

    def update(self, *args):
        self.rect = self.rect.move(*self.speed)

    def intersect(self, obj_rect):
        edges = dict(
            left=Rect(obj_rect.left, obj_rect.top, 1, obj_rect.height),
            right=Rect(obj_rect.right, obj_rect.top, 1, obj_rect.height),
            top=Rect(obj_rect.left, obj_rect.top, obj_rect.width, 1),
            bottom=Rect(obj_rect.left, obj_rect.bottom, obj_rect.width, 1),
        )
        collisions = set(edge for edge, rect in edges.items() if self.rect.colliderect(rect))

        if not collisions:
            return None

        if len(collisions) == 1:
            return list(collisions)[0]

        if 'top' in collisions:
            if self.rect.centery >= obj_rect.top:
                return 'top'
            elif self.rect.centerx >= obj_rect.left:
                return 'left'
            else:
                return 'right'

        if 'bottom' in collisions:
            if self.rect.centery >= obj_rect.bottom:
                return 'bottom'
            elif self.rect.centerx < obj_rect.left:
                return 'left'
            else:
                return 'right'


class Brick(Sprite):
    BRICK_WIDTH = 80
    BRICK_HEIGHT = 20
    BRICK_COLOR = 0, 0, 255

    def __init__(self, x, y, effect=None):
        super().__init__()
        self.rect = Rect(
            x * (self.BRICK_WIDTH + 1),
            y * (self.BRICK_HEIGHT + 1),
            self.BRICK_WIDTH,
            self.BRICK_HEIGHT,
        )
        self.image = pygame.Surface((self.rect.width, self.rect.height))

        self.color = self.BRICK_COLOR
        self.effect = effect

        self.image.fill(self.color)


class BaseScreen(pygame.Surface):
    def __init__(self, game):
        super().__init__((game.width, game.height))
        self.game = game
        self.background = game.background
        self.background_pos = game.background_pos

        self.sprites = Group()

    def update(self):
        self.sprites.update()

    def draw(self):
        self.blit(self.background, self.background_pos)
        self.sprites.draw(self)


class MenuScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.create_menu()

    def create_menu(self):
        menu_items = [
            MenuItem(item_id, text, handler)
            for item_id, (text, handler) in enumerate((
                ('PLAY', self.on_play),
                ('QUIT', self.on_quit),
            ))
        ]

        self.sprites.add(*menu_items)

        for menu_item in menu_items:
            self.game.mouse_handlers.append(menu_item.handle_mouse_event)

    def on_play(self, button):
        self.game.set_state(self.game.STATE_PLAYING)

    def on_quit(self, button):
        self.game.set_state(self.game.STATE_GAME_OVER)


class GameScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.lives = 5
        self.score = 0
        self.points_per_brick = 10

        self.paddle = Paddle(self.get_rect())
        self.bricks = Group([
            Brick(i, j)
            for i in range(10)
            for j in range(5)
        ])
        self.ball = None

        self.sprites.add(self.paddle, *self.bricks)
        self.create_ball()

        self.game.keydown_handlers[pygame.K_LEFT] = self.paddle.handle,
        self.game.keydown_handlers[pygame.K_RIGHT] = self.paddle.handle,
        self.game.keyup_handlers[pygame.K_LEFT] = self.paddle.handle,
        self.game.keyup_handlers[pygame.K_RIGHT] = self.paddle.handle,

    def update(self):
        super().update()

        if not self.bricks:
            return self.game.set_state(self.game.STATE_WIN)

        self.handle_ball_collisions()

    def create_ball(self):
        self.ball = Ball(self.game.width // 2, self.game.height // 2)
        self.sprites.add(self.ball)

    def handle_ball_collisions(self):
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

        if self.ball.rect.top > self.game.height:
            self.lives -= 1
            if self.lives <= 0:
                self.game.state = self.game.STATE_GAME_OVER
            else:
                self.create_ball()

        if self.ball.rect.top < 0:
            self.ball.speed = speed[0], -speed[1]

        if self.ball.rect.left < 0 or self.ball.rect.right >= self.game.width:
            self.ball.speed = -speed[0], speed[1]

        for brick in self.bricks:
            brick_edge = self.ball.intersect(brick.rect)
            if not brick_edge:
                continue

            # self.sound_effects['brick_hit'].play()

            self.bricks.remove(brick)
            self.sprites.remove(brick)
            self.score += self.points_per_brick

            if brick_edge in ('top', 'bottom'):
                self.ball.speed = speed[0], -speed[1]
            else:
                self.ball.speed = -speed[0], speed[1]


class Breakout(Game):
    MESSAGE_DURATION = 5

    STATE_WIN = 10

    def __init__(self, **config):
        super().__init__(**config)

        # self.sound_effects = {
        #     name: pygame.mixer.Sound(sound)
        #     for name, sound in config.SOUND_EFFECTS.items()
        # }
        # music = pygame.mixer.music.load('music.mp3')
        # pygame.mixer.music.play(-1, 0.0)

        self.screen = None
        self.background = pygame.image.load('../res/global/map.jpg')
        self.set_state(self.STATE_MENU)

    def update(self):
        super().update()
        if self.screen is not None:
            self.screen.update()

    def draw(self):
        super().draw()
        self.screen.draw()
        if self.screen is not None:
            self.surface.blit(self.screen, (0, 0))

    def set_state(self, state):
        if self.state == state:
            return

        self.state = state

        if self.state == self.STATE_MENU:
            self.screen = MenuScreen(self)
        if self.state == self.STATE_PLAYING:
            self.screen = GameScreen(self)
        if self.state == self.STATE_WIN:
            self.show_message("YOU WIN!!!", center=True)
            self.set_state(self.STATE_GAME_OVER)
        if self.state == self.STATE_GAME_OVER:
            self.set_state(self.STATE_EXIT)

    def show_message(
        self,
        text,
        color=(255, 255, 255),
        font_name='Arial',
        font_size=20,
        center=False,
    ):
        message = TextObject(
            self.width // 2,
            self.height // 2,
            lambda: text,
            Font(
                font_name,
                font_size,
                color,
            ),
        )
        self.draw()
        message.draw(self.surface, center)
        pygame.display.update()
        time.sleep(self.MESSAGE_DURATION)
