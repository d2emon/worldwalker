#! /usr/bin/python
import config
import pygame
from player import Player
from bgmap import BgMap
from background import Background
from grid import MapGrid
from pygame.time import Clock


CONTROLS = {
    pygame.K_LEFT: (-1, None),
    pygame.K_RIGHT: (1, None),
    pygame.K_UP: (None, -1),
    pygame.K_DOWN: (None, 1),
}


def main():
    pygame.init()
    screen = pygame.display.set_mode(config.DISPLAY)
    pygame.display.set_caption(config.TITLE)

    pygame.font.init()
    myfont = pygame.font.SysFont('Sans', 16)

    bg = Background((config.WIN_WIDTH, config.WIN_HEIGHT))

    game_map = BgMap(*config.MAP_POS)
    hero = Player(*config.PLAYER_POS)
    xvel = yvel = 0

    show_grid = False
    map_grid = MapGrid(game_map.rect.width, game_map.rect.height, config.GRID_SIZE)

    timer = Clock()

    while True:
        for event in pygame.event.get():
            event_exit(event)
            xvel, yvel = event_move(event, xvel, yvel)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                game_map.x = config.MAP_POS[0]
                game_map.y = config.MAP_POS[1]
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                show_grid = not show_grid

        bg.draw(screen)

        game_map.update(xvel, yvel)
        game_map.draw(screen)

        if show_grid:
            map_grid.draw(screen)

        hero.draw(screen)

        coords = "{}, {}".format(game_map.x, game_map.y)
        text_surface = myfont.render(coords, False, (0, 0, 0))
        screen.blit(text_surface, (0, 0))

        pygame.display.update()
        timer.tick(24)


def event_exit(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        raise SystemExit("QUIT")
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        raise SystemExit("QUIT")


def event_move(event, xvel, yvel):
    if event.type == pygame.KEYDOWN and event.key in CONTROLS.keys():
        c = CONTROLS[event.key]
        if c[0] is not None:
            xvel = c[0]
        if c[1] is not None:
            yvel = c[1]

    if event.type == pygame.KEYUP and event.key in CONTROLS.keys():
        c = CONTROLS[event.key]
        if c[0] is not None:
            xvel = 0
        if c[1] is not None:
            yvel = 0
    return xvel, yvel


if __name__ == "__main__":
    main()
