#! /usr/bin/python
import config
import pygame
from pygame.locals import *
from player import Player
from pygame.time import Clock


CONTROLS = {
    K_LEFT: (-1, None),
    K_RIGHT: (1, None),
    K_UP: (None, -1),
    K_DOWN: (None, 1),
}


def main():
    pygame.init()
    screen = pygame.display.set_mode(config.DISPLAY)
    pygame.display.set_caption('Hello World Play!')

    bg_img = pygame.image.load('../res/global/map.jpg')
    bg = pygame.Surface((config.WIN_WIDTH, config.WIN_HEIGHT))
    # bg.fill(pygame.Color(config.BACKGROUND_COLOR))
    bg.blit(bg_img, (0, 0))

    timer = Clock()

    hero = Player(10, 10)
    xvel = yvel = 0

    while True:
        timer.tick(60)
        for event in pygame.event.get():
            event_exit(event)
            xvel, yvel = event_move(event, xvel, yvel)

        screen.blit(bg, (0, 0))

        hero.update(xvel, yvel)
        hero.draw(screen)

        pygame.display.update()


def event_exit(event):
    if event.type == QUIT:
        pygame.quit()
        raise SystemExit("QUIT")
    if event.type == KEYDOWN and event.key == K_ESCAPE:
        raise SystemExit("QUIT")


def event_move(event, xvel, yvel):
    if event.type == KEYDOWN and event.key in CONTROLS.keys():
        c = CONTROLS[event.key]
        if c[0] is not None:
            xvel = c[0]
        if c[1] is not None:
            yvel = c[1]

    if event.type == KEYUP and event.key in CONTROLS.keys():
        c = CONTROLS[event.key]
        if c[0] is not None:
            xvel = 0
        if c[1] is not None:
            yvel = 0
    return xvel, yvel


if __name__ == "__main__":
    main()
