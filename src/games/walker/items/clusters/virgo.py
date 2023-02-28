"""Virgo Supercluster."""

from ..circular import Circular


class VirgoSupercluster(Circular):
    """item sprite."""

    name = 'Virgo Supercluster'
    base_scale = 21 + 2
    base_size = 2.80
    color = (0, 0, 255)


class VirgoCluster(Circular):
    """item sprite."""

    name = 'Virgo Cluster'
    base_scale = 21 + 2
    base_size = 1.30
    color = (0, 0, 255)
