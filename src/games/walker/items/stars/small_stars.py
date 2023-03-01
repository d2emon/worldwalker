"""Stars."""

from ..circular import Circular


def color(value):
    return value, value, 0


class Star(Circular):
    """Item sprite."""
    base_scale = 9
    color = color(255)
    label_color = (255, 255, 255)


class Regulus(Star):
    """Item sprite."""
    name = 'Regulus'
    base_size = 6.1
    color = color(255)


class Vega(Star):
    """Item sprite."""
    name = 'Vega'
    base_size = 3.5
    color = color(255)


class Altair(Star):
    """Item sprite."""
    name = 'Altair'
    base_size = 2.8
    color = color(255)


class Pollux(Star):
    """Item sprite."""
    name = 'Pollux'
    base_size = 2.7
    color = color(255)


class SiriusA(Star):
    """Item sprite."""
    name = 'Sirius A'
    base_size = 2.3
    color = color(255)


class Procyon(Star):
    """Item sprite."""
    name = 'Procyon'
    base_size = 2.8
    color = color(255)


class AlphaCentauriA(Star):
    """Item sprite."""
    name = 'Alpha Centauri A'
    base_size = 1.7
    color = color(255)


class AlphaCentauriB(Star):
    """Item sprite."""
    name = 'Alpha Centauri B'
    base_size = 1.2
    color = color(255)


class Sun(Star):
    """Item sprite."""
    name = 'Sun'
    base_size = 1.4
    color = color(255)
