from ..circular import Circular


class SuperclusterComplex(Circular):
    """item sprite."""
    base_scale = 24 + 1
    color = (0, 0, 255)


class Cluster(Circular):
    """item sprite."""
    base_scale = 21 + 2
    color = (0, 0, 255)


class GalaxyGroup(Circular):
    """item sprite."""
    base_scale = 21 + 1
    color = (0, 0, 255)


CLUSTERS = [
    SuperclusterComplex('Pisces-Cetus Supercluster Complex', size=1.0),
    Cluster('Virgo Supercluster', size=2.80),
    Cluster('Virgo Cluster', size=1.30),
    Cluster('Fornax Cluster', size=2.00),
    GalaxyGroup('Local Group', size=9.50),
    GalaxyGroup('Abell 2029', size=6.00),
]
