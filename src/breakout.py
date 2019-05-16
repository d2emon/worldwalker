import random
import time
import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite, Group
from game_utils import Game, GameObject, TextObject


class Font:
    def __init__(self, name='Arial', size=10, color=(0, 0, 0)):
        self.name = name
        self.size = size
        self.color = color


class Button(Sprite):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2

    COLORS = {
        NORMAL: (255, 255, 255),
        HOVER: (0, 255, 255),
        PRESSED: (0, 0, 255),
    }

    DEFAULT_FONT = Font()

    def __init__(self, rect, text, on_click=lambda x: None, padding=0, font=DEFAULT_FONT):
        super().__init__()
        self.state = self.NORMAL
        self.rect = rect
        self.text = TextObject(
            padding,
            padding,
            lambda: text,
            font,
        )
        self.on_click = on_click
        self.image = pygame.Surface((self.rect.width, self.rect.height))

    @property
    def background_color(self):
        return self.COLORS[self.state]

    def update(self, *args):
        self.image.fill(self.background_color)
        self.text.draw(self.image)

    def handle_mouse_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.handle_mouse_move(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(event)

    def handle_mouse_move(self, event):
        if self.rect.collidepoint(event.pos):
            if self.state != self.PRESSED:
                self.state = self.HOVER
        else:
            self.state = self.NORMAL

    def handle_mouse_down(self, event):
        if self.rect.collidepoint(event.pos):
            self.state = self.PRESSED

    def handle_mouse_up(self, event):
        if self.state == self.PRESSED:
            self.on_click(self)
            self.state = self.HOVER


class Paddle(GameObject):
    def __init__(self, x, y, w, h, color, offset, max_x):
        super().__init__(x, y, w, h)
        self.color = color
        self.offset = offset
        self.moving_left = False
        self.moving_right = False
        self.max_x = max_x

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def handle(self, event):
        if event.key == pygame.K_LEFT:
            self.moving_left = not self.moving_left
        else:
            self.moving_right = not self.moving_right

    def update(self):
        if self.moving_left:
            dx = -min(self.offset, self.left)
        elif self.moving_right:
            dx = min(self.offset, self.max_x - self.right)
        else:
            return

        self.move(dx, 0)


class Ball(GameObject):
    def __init__(self, x, y, r, color, speed):
        super().__init__(x - r, y - r, r * 2, r * 2, speed)
        self.radius = r
        self.color = color

    @property
    def diameter(self):
        return self.radius * 2

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.radius)


class Brick(GameObject):
    def __init__(self, x, y, w, h, color, effect=None):
        super().__init__(x, y, w, h)
        self.color = color
        self.effect = effect

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Breakout(Game):
    PADDLE_X = 300
    PADDLE_Y = 400
    PADDLE_W = 80
    PADDLE_H = 20
    PADDLE_COLOR = 255, 0, 0
    PADDLE_OFFSET = 10

    MENU_OFFSET_X = 5
    MENU_OFFSET_Y = 5
    MENU_BUTTON_W = 200
    MENU_BUTTON_H = 20

    BALL_SPEED = 1
    BALL_RADIUS = 5
    BALL_COLOR = 0, 255, 0

    BRICK_WIDTH = 80
    BRICK_HEIGHT = 20
    BRICK_COLOR = 0, 0, 255

    MESSAGE_DURATION = 5

    def __init__(self, **config):
        super().__init__(**config)

        # self.sound_effects = {
        #     name: pygame.mixer.Sound(sound)
        #     for name, sound in config.SOUND_EFFECTS.items()
        # }
        # music = pygame.mixer.music.load('music.mp3')
        # pygame.mixer.music.play(-1, 0.0)

        self.background = pygame.image.load('../res/global/map.jpg')

        self.sprites = Group()
        self.menu = Group()

        self.paddle = self.create_paddle()
        self.ball = None
        self.bricks = []

        self.lives = 5
        self.score = 0
        self.points_per_brick = 10
        self.create_menu()

        self.keydown_handlers[pygame.K_LEFT] = self.paddle.handle,
        self.keydown_handlers[pygame.K_RIGHT] = self.paddle.handle,
        self.keyup_handlers[pygame.K_LEFT] = self.paddle.handle,
        self.keyup_handlers[pygame.K_RIGHT] = self.paddle.handle,

        self.state = self.STATE_MENU

    def update(self):
        super().update()

        self.sprites.update()

        if self.state == self.STATE_MENU:
            return
        elif self.state == self.STATE_PLAYING:
            if not self.bricks:
                self.show_message("YOU WIN!!!", center=True)
                self.state = self.STATE_GAME_OVER
                print(self.state)
                return
            self.handle_ball_collisions()
        elif self.state == self.STATE_GAME_OVER:
            self.state = self.STATE_EXIT
            return
        elif self.state == self.STATE_EXIT:
            return

    def draw(self):
        super().draw()
        self.sprites.draw(self.surface)

    def create_menu(self):
        def on_play(button):
            for item in self.menu:
                self.sprites.remove(item)

            self.objects.append(self.paddle)

            for i in range(10):
                for j in range(5):
                    self.create_brick(i, j)

            self.create_ball()

            self.state = self.STATE_PLAYING

        def on_quit(button):
            self.state = self.STATE_GAME_OVER

        for i, (text, handler) in enumerate((
            ('PLAY', on_play),
            ('QUIT', on_quit),
        )):
            button = Button(
                Rect(
                    self.MENU_OFFSET_X,
                    self.MENU_OFFSET_Y + (self.MENU_BUTTON_H + 5) * i,
                    self.MENU_BUTTON_W,
                    self.MENU_BUTTON_H,
                ),
                text,
                handler,
                padding=5,
            )
            self.menu.add(button)
            self.sprites.add(button)
            self.mouse_handlers.append(button.handle_mouse_event)

    def create_paddle(self):
        return Paddle(
            self.PADDLE_X,
            self.PADDLE_Y,
            self.PADDLE_W,
            self.PADDLE_H,
            self.PADDLE_COLOR,
            self.PADDLE_OFFSET,
            self.width,
        )

    def create_ball(self):
        speed = random.randint(-2, 2), self.BALL_SPEED
        self.ball = Ball(self.width // 2, self.height // 2, self.BALL_RADIUS, self.BALL_COLOR, speed)
        self.objects.append(self.ball)

    def create_brick(self, x, y):
        brick = Brick(
            x * (self.BRICK_WIDTH + 1),
            y * (self.BRICK_HEIGHT + 1),
            self.BRICK_WIDTH,
            self.BRICK_HEIGHT,
            self.BRICK_COLOR,
        )
        self.bricks.append(brick)
        self.objects.append(brick)

    def handle_ball_collisions(self):
        def intersect(obj, ball):
            edges = dict(
                left=Rect(obj.left, obj.top, 1, obj.height),
                right=Rect(obj.right, obj.top, 1, obj.height),
                top=Rect(obj.left, obj.top, obj.width, 1),
                bottom=Rect(obj.left, obj.bottom, obj.width, 1),
            )
            collisions = set(edge for edge, rect in edges.items() if ball.rect.colliderect(rect))

            if not collisions:
                return None

            if len(collisions) == 1:
                return list(collisions)[0]

            if 'top' in collisions:
                if ball.centery >= obj.top:
                    return 'top'
                elif ball.centerx >= obj.left:
                    return 'left'
                else:
                    return 'right'

            if 'bottom' in collisions:
                if ball.centery >= obj.bottom:
                    return 'bottom'
                elif ball.centerx < obj.left:
                    return 'left'
                else:
                    return 'right'

        speed = self.ball.speed
        edge = intersect(self.paddle, self.ball)
        # if edge is not None:
        #     self.sound_effects['paddle_hit'].play()

        if edge == 'top':
            speed_x = speed[0]
            speed_y = -speed[1]
            if self.paddle.moving_left:
                speed_x -= 1
            elif self.paddle.moving_right:
                speed_x += 1
            self.ball.speed = speed_x, speed_y
        elif edge in ('left', 'right'):
            self.ball.speed = -speed[0], speed[1]

        if self.ball.top > self.height:
            self.lives -= 1
            if self.lives <= 0:
                self.state = self.STATE_GAME_OVER
            else:
                self.create_ball()

        if self.ball.top < 0:
            self.ball.speed = speed[0], -speed[1]

        if self.ball.left < 0 or self.ball.right >= self.width:
            self.ball.speed = -speed[0], speed[1]

        if not self.bricks:
            self.show_message("YOU WIN!!!", center=True)
            self.state = self.STATE_GAME_OVER
            return

        for brick in self.bricks:
            edge = intersect(brick, self.ball)
            if not edge:
                continue

            # self.sound_effects['brick_hit'].play()

            self.bricks.remove(brick)
            self.objects.remove(brick)
            self.score += self.points_per_brick

            if edge in ('top', 'bottom'):
                self.ball.speed = speed[0], -speed[1]
            else:
                self.ball.speed = -speed[0], speed[1]

    def show_message(
        self,
        text,
        color=(255, 255, 255),
        font_name='Arial',
        font_size=20,
        center=False,
    ):
        print(text)
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
