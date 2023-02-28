"""Nebulas."""

from ..circular import Circular


def color(value):
    return value, 0, 0


class Nebula(Circular):
    """Item sprite."""
    base_scale = 15 + 1
    color = color(128)
    label_color = (0, 0, 0)


class BlackPillar(Nebula):
    """Item sprite."""
    name = 'Black Pillar Nebula'
    base_size = 9.0
    color = color(120)


class Cone(Nebula):
    """Item sprite."""
    name = 'Cone Nebula'
    base_size = 8.0
    color = color(112)


class Bubble(Nebula):
    """Item sprite."""
    name = 'Bubble Nebula'
    base_size = 7.0
    color = color(104)


class Horsehead(Nebula):
    """Item sprite."""
    name = 'Horsehead Nebula'
    base_size = 6.6
    color = color(96)


class CatsEye(Nebula):
    """Item sprite."""
    name = 'Cat\'s Eye Nebula'
    base_size = 6.1
    color = color(88)


class Helix(Nebula):
    """Item sprite."""
    name = 'Helix Nebula'
    base_size = 5.4
    color = color(80)


class PillarsOfCreation(Nebula):
    """Item sprite."""
    name = 'Pillars of Creation'
    base_size = 3.8
    color = color(72)


class Ring(Nebula):
    """Item sprite."""
    name = 'Ring Nebula'
    base_size = 2.4
    color = color(66)


class Boomerang(Nebula):
    """Item sprite."""
    name = 'Boomerang Nebula'
    base_size = 1.9
    color = color(58)


class Escimo(Nebula):
    """Item sprite."""
    name = 'Escimo Nebula'
    base_size = 1.5
    color = color(50)


class Ant(Nebula):
    """Item sprite."""
    name = 'Ant Nebula'
    base_size = 2.0
    color = color(42)
