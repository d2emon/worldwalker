"""Stars."""

from ..circular import Circular


def color(value):
    return value, 0, 0


class Star(Circular):
    """Item sprite."""
    base_scale = 9 + 1
    color = color(255)
    label_color = (255, 255, 255)


class Albireo(Star):
    """Item sprite."""
    name = 'Albireo'
    base_size = 8.6
    color = color(255)


class Aldebaran(Star):
    """Item sprite."""
    name = 'Aldebaran'
    base_size = 6.3
    color = color(255)


class Polaris(Star):
    """Item sprite."""
    name = 'Polaris'
    base_size = 5.2
    color = color(255)


class Arcturus(Star):
    """Item sprite."""
    name = 'Arcturus'
    base_size = 3.6
    color = color(255)


class Alnitak(Star):
    """Item sprite."""
    name = 'Alnitak'
    base_size = 2.8
    color = color(255)


class Capella(Star):
    """Item sprite."""
    name = 'Capella'
    base_size = 1.7
    color = color(255)


class Spica(Star):
    """Item sprite."""
    name = 'Spica'
    base_size = 1.0
    color = color(255)
