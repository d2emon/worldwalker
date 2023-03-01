"""Stars."""

from ..circular import Circular


def color(value):
    return value, 0, 0


class Star(Circular):
    """Item sprite."""
    base_scale = 9 + 2
    color = color(255)
    label_color = (255, 255, 255)


class V354Cephei(Star):
    """Item sprite."""
    name = 'V354 Cephei'
    base_size = 9.50
    color = color(255)


class Antares(Star):
    """Item sprite."""
    name = 'Antares'
    base_size = 9.70
    color = color(255)


class LaSuperba(Star):
    """Item sprite."""
    name = 'La Superba'
    base_size = 5.90
    color = color(255)


class SDoradus(Star):
    """Item sprite."""
    name = 'S Doradus'
    base_size = 5.30
    color = color(255)


class RDoradus(Star):
    """Item sprite."""
    name = 'R Doradus'
    base_size = 4.10
    color = color(255)


class Enif(Star):
    """Item sprite."""
    name = 'Enif'
    base_size = 2.90
    color = color(255)


class Deneb(Star):
    """Item sprite."""
    name = 'Enif'
    base_size = 2.80
    color = color(255)


class Cacrux(Star):
    """Item sprite."""
    name = 'Cacrux'
    base_size = 1.70
    color = color(255)


class Rigel(Star):
    """Item sprite."""
    name = 'Rigel'
    base_size = 1.10
    color = color(255)
