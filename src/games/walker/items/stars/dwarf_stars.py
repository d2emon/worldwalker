"""Stars."""

from ..circular import Circular


def color(value):
    return value, value, 0


class Star(Circular):
    """Item sprite."""
    base_scale = 6 + 2
    color = color(255)
    label_color = (0, 0, 0)


class Gliese229A(Star):
    """Item sprite."""
    name = 'Gliese 229A'
    base_size = 9.60
    color = color(255)


class Luyten(Star):
    """Item sprite."""
    name = 'Luyten\'s Star'
    base_size = 4.90
    color = color(255)


class Kapteyn(Star):
    """Item sprite."""
    name = 'Kapteyn\'s Star'
    base_size = 4.00
    color = color(255)


class ProximaCentauri(Star):
    """Item sprite."""
    name = 'Proxima Centauri'
    base_size = 2.10
    color = color(255)


class Wolf359(Star):
    """Item sprite."""
    name = 'Wolf 359'
    base_size = 2.00
    color = color(255)


class Gliese229B(Star):
    """Item sprite."""
    name = 'Gliese 229B'
    base_size = 1.60
    color = color(255)


class SiriusB(Star):
    """Item sprite."""
    name = 'Sirius B'
    base_scale = 6 + 1
    base_size = 1.10
    color = color(255)


class NeutronStar(Star):
    """Item sprite."""
    name = 'Neutron Star'
    base_scale = 3 + 1
    base_size = 2.40
    color = (255, 255, 255)
