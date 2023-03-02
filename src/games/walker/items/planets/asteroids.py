"""Asteroids."""

from ..circular import Circular


class Asteroid(Circular):
    """Item sprite."""
    base_scale = 3 + 2
    color = (0, 192, 255)
    label_color = (255, 255, 255)


class Ceres(Asteroid):
    """Item sprite."""
    name = 'Ceres'
    base_size = 9.50


class Hydra(Asteroid):
    """Item sprite."""
    name = 'Hydra'
    base_size = 4.00


class Dysnomia(Asteroid):
    """Item sprite."""
    name = 'Dysnomia'
    base_size = 1.40


class Nix(Asteroid):
    """Item sprite."""
    name = 'Nix'
    base_scale = 3 + 1
    base_size = 3.5


class Phobos(Asteroid):
    """Item sprite."""
    name = 'Phobos'
    base_scale = 3 + 1
    base_size = 2.3


class Deimos(Asteroid):
    """Item sprite."""
    name = 'Deimos'
    base_scale = 3 + 1
    base_size = 1.3


class Cruithne(Asteroid):
    """Item sprite."""
    name = 'Cruithne'
    base_scale = 3
    base_size = 5
