"""Continents."""

from ..square import Square


class Continent(Square):
    """Item sprite."""
    base_scale = 6
    color = (0, 255, 0)
    label_color = (255, 255, 255)


class Asia(Continent):
    """Item sprite."""
    name = 'Asia'
    base_size = 8
