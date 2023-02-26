"""Constants for controls."""

import pygame


CONTROLS = {
    pygame.K_LEFT: (-1, None),
    pygame.K_RIGHT: (1, None),
    pygame.K_UP: (None, -1),
    pygame.K_DOWN: (None, 1),
}
