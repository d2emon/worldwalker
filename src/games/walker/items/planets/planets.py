"""Planets."""

from ..circular import Circular


class Planet(Circular):
    """Item sprite."""
    base_scale = 6
    color = (0, 192, 255)
    label_color = (255, 255, 255)


class Earth(Planet):
    """Item sprite."""
    name = 'Earth'
    base_scale = 6 + 1
    base_size = 1.27


class Venus(Planet):
    """Item sprite."""
    name = 'Venus'
    base_scale = 6 + 1
    base_size = 1.20


class Mars(Planet):
    """Item sprite."""
    name = 'Mars'
    base_size = 6.8


class Mercury(Planet):
    """Item sprite."""
    name = 'Mercury'
    base_size = 4.9


class Ganymede(Planet):
    """Item sprite."""
    name = 'Ganymede'
    base_size = 5.3


class Callisto(Planet):
    """Item sprite."""
    name = 'Callisto'
    base_size = 4.8


class Titan(Planet):
    """Item sprite."""
    name = 'Titan'
    base_size = 5.2


class Io(Planet):
    """Item sprite."""
    name = 'Io'
    base_size = 3.6


class Europa(Planet):
    """Item sprite."""
    name = 'Europa'
    base_size = 3.1


class Moon(Planet):
    """Item sprite."""
    name = 'Moon'
    base_size = 3.5


class Triton(Planet):
    """Item sprite."""
    name = 'Triton'
    base_size = 2.7


class Eris(Planet):
    """Item sprite."""
    name = 'Eris'
    base_size = 2.33


class Pluto(Planet):
    """Item sprite."""
    name = 'Pluto'
    base_size = 2.3


class Charon(Planet):
    """Item sprite."""
    name = 'Charon'
    base_size = 1.2


class Quaoar(Planet):
    """Item sprite."""
    name = 'Quaoar'
    base_size = 1.1


class Sedna(Planet):
    """Item sprite."""
    name = 'Sedna'
    base_size = 1.0
