"""Nebulas."""

from ..circular import Circular


def color(value):
    return value, value, 0


class Nebula(Circular):
    """Item sprite."""
    base_scale = 15
    color = color(255)
    label_color = (0, 0, 0)


class Homunculus(Nebula):
    """Item sprite."""
    name = 'Homunculus Nebula'
    base_size = 5.5
    color = color(255)


class Hourglass(Nebula):
    """Item sprite."""
    name = 'Hourglass Nebula'
    base_size = 5.5
    color = color(248)


class Blinking(Nebula):
    """Item sprite."""
    name = 'Blinking Nebula'
    base_size = 4.5
    color = color(240)


class Stingray(Nebula):
    """Item sprite."""
    name = 'Stingray Nebula'
    base_size = 1.5
    color = color(232)


class HomezHamburger(Nebula):
    """Item sprite."""
    name = 'Homez\'s Hamburger'
    base_scale = 12 + 2
    base_size = 4.70
    color = color(224)
