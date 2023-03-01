"""Nebulas."""

from .circular import Circular
from .distance import Distance


class OortsCloud(Circular):
    """Item sprite."""
    name = 'Oort\'s Cloud'
    base_scale = 15 + 1
    base_size = 1.8
    color = (255, 255, 255)
    label_color = (0, 0, 0)


class KuipersBelt(Circular):
    """Item sprite."""
    name = 'Kuiper\'s Belt'
    base_scale = 12 + 1
    base_size = 1.2
    color = (255, 255, 255)
    label_color = (0, 0, 0)


class DistanceFromVoyager(Distance):
    """item sprite."""

    name = 'Distance from Voyager 1 to Earth'
    base_scale = 12 + 1
    color = (0, 255, 0)
    radius = 2.3


class DistanceFromNeptune(Distance):
    """item sprite."""

    name = 'Distance from Neptune to Sun'
    base_scale = 12
    color = (0, 255, 0)
    radius = 4.47


class DistanceFromEarth(Distance):
    """item sprite."""

    name = 'Distance from Earth to Sun'
    base_scale = 9 + 2
    color = (0, 255, 0)
    radius = 1.50


class DistanceToMoon(Distance):
    """item sprite."""

    name = 'Distance from Earth to Moon'
    base_scale = 6 + 2
    color = (0, 255, 0)
    radius = 3.80
