"""Stars."""

from ..circular import Circular


def color(value):
    return value, 0, 0


class Star(Circular):
    """Item sprite."""
    base_scale = 12
    color = color(255)
    label_color = (255, 255, 255)


class WOHG64(Star):
    """Item sprite."""
    name = 'WOH G64'
    base_size = 2.1
    color = color(255)


class VYCanisMajoris(Star):
    """Item sprite."""
    name = 'VY Canis Majoris'
    base_size = 2.0
    color = color(255)


class KYCygni(Star):
    """Item sprite."""
    name = 'KY Cygni'
    base_size = 1.4
    color = color(255)


class MuCephei(Star):
    """Item sprite."""
    name = 'Mu Cephei'
    base_size = 1.4
    color = color(255)


class Betelgeuse(Star):
    """Item sprite."""
    name = 'Betelgeuse'
    base_size = 1.1
    color = color(255)


class VVCepheiA(Star):
    """Item sprite."""
    name = 'VV Cephei A'
    base_size = 1.1
    color = color(255)


class Pistol(Star):
    """Item sprite."""
    name = 'Pistol Star'
    base_size = 1.2
    color = color(255)
