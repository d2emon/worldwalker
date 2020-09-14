import os
from . import files
from .screen import Screen


SCREEN = Screen(
    800,  # 640
    600,  # 460  # 640
    "World Walker",
)

FPS = 60

PLAYER_POS = SCREEN.CENTER
MAP_POS = (0, 0)
BACKGROUND_COLOR = "#0099FF"
FRAME_RATE = 60
GRID_SIZE = 32

MAP_FILE = files.MAP_FILE
MAP_SCALE = 0.5

SCALE = int(100 * MAP_SCALE)
TIME_SCALE = 5 / 60

X0, Y0 = 10, 35
VIEWPOINT = (33.5 * SCALE + X0, 7.5 * SCALE + Y0)

PLAYER_SIZE = 10
PLAYER_VIEW = 5 * SCALE
PLAYER_COLOR = (255, 255, 0)
PLAYER_VIEW_COLOR = (0, 0, 255)
