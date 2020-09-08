import pygame
from pygame.sprite import Sprite
from .text_object import Font, TextObject


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
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))

        self.state = self.NORMAL
        self.text = TextObject(
            padding,
            padding,
            lambda: text,
            font,
        )
        self.on_click = on_click

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
