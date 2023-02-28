"""Nebulas."""

from ..circular import Circular


def color(value):
    return value, 0, 0


class Nebula(Circular):
    """Item sprite."""
    base_scale = 18
    color = color(255)
    label_color = (0, 0, 0)


class Tarantula(Nebula):
    """Item sprite."""
    name = 'Tarantula Nebula'
    base_scale = 18 + 1
    base_size = 1.8
    color = color(255)


class BarnardsLoop(Nebula):
    """Item sprite."""
    name = 'Barnard\'s Loop'
    base_size = 9.4
    color = color(248)


class Carina(Nebula):
    """Item sprite."""
    name = 'Great Nebula in Carina'
    base_size = 4.4
    color = color(240)


class Rosette(Nebula):
    """Item sprite."""
    name = 'Rosette Nebula'
    base_size = 1.2
    color = color(232)


class Eagle(Nebula):
    """Item sprite."""
    name = 'Eagle Nebula'
    base_size = 1.2
    color = color(232)
