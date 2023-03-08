from ..circular import Circular


class GalaxyGroup(Circular):
    """item sprite."""
    base_scale = 21 + 1
    color = (255, 255, 255, 128)
    label_color = (0, 0, 0)


class Cluster(GalaxyGroup):
    """item sprite."""
    base_scale = 21 + 2


class SuperclusterComplex(GalaxyGroup):
    """item sprite."""
    base_scale = 24 + 1


CLUSTERS = [
    SuperclusterComplex('Pisces-Cetus Supercluster Complex', size=1.0, visible=False),
    Cluster('Virgo Supercluster', size=2.80, visible=False),
    Cluster('Virgo Cluster', size=1.30, visible=False),
    Cluster('Fornax Cluster', size=2.00, visible=False),
    GalaxyGroup('Local Group', size=9.50, visible=False),
    GalaxyGroup('Abell 2029', size=6.00, visible=False),
]
