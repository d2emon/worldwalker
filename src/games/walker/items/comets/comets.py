"""Comets."""

from ..circular import Circular


class Comet(Circular):
    """Item sprite."""
    base_scale = 3 + 1
    color = (0, 192, 255)
    label_color = (255, 255, 255)


class HalleysComet(Comet):
    """Item sprite."""
    name = 'Halley\'s Comet'
    base_size = 1.1
