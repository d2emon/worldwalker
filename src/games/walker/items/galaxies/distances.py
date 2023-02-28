"""Distances sprites."""

from ..distance import Distance


class DistanceToAndromedaGalaxy(Distance):
    """Item sprite."""

    name = 'Distance to Andromeda Galaxy'
    base_scale = 21 + 1
    radius = 2.3
    color = (0, 255, 0)


class DistanceEarthTravelled(Distance):
    """Item sprite."""

    name = 'Distance Earth has Travelled (Relative to Sun)'
    base_scale = 21
    radius = 4.5
    color = (0, 255, 0)
