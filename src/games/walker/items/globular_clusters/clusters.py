"""Nebulas."""

from ..circular import Circular


def color(value):
    return value, value, value


class GlobularCluster(Circular):
    """Item sprite."""
    base_scale = 18
    color = color(255)
    label_color = (0, 0, 0)


class Messier54(GlobularCluster):
    """Item sprite."""
    name = 'Messier 54'
    base_size = 2.9
    color = color(255)


class OmegaCentauri(GlobularCluster):
    """Item sprite."""
    name = 'Omega Centauri'
    base_size = 1.6
    color = color(248)
