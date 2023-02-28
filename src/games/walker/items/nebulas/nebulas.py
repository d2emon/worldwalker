"""Nebulas."""

from ..circular import Circular


def color(value):
    return value, 0, 0


class Nebula(Circular):
    """Item sprite."""
    base_scale = 15 + 2
    color = color(196)
    label_color = (0, 0, 0)


class NorthAmerica(Nebula):
    """Item sprite."""
    name = 'North America Nebula'
    base_size = 9.50
    color = color(196)


class Cave(Nebula):
    """Item sprite."""
    name = 'Cave Nebula'
    base_size = 7.00
    color = color(188)


class Lagoon(Nebula):
    """Item sprite."""
    name = 'Cave Nebula'
    base_size = 3.30
    color = color(180)


class Orion(Nebula):
    """Item sprite."""
    name = 'Orion Nebula'
    base_size = 2.30
    color = color(172)


class RottenEgg(Nebula):
    """Item sprite."""
    name = 'Rotten Egg Nebula'
    base_size = 1.30
    color = color(164)


class Crab(Nebula):
    """Item sprite."""
    name = 'Crab Nebula'
    base_size = 1.10
    color = color(156)
