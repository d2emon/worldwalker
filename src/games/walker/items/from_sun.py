"""Distance to Proxima Centauri."""

from .distance import Distance


class DistanceFromSunToProximaCentauri(Distance):
    """item sprite."""

    name = 'Distance from Sun to Proxima Centauri'
    base_scale = 15 + 1
    color = (0, 255, 0)
    radius = 4.0



class DistanceFromAlphaToProximaCentauri(Distance):
    """item sprite."""

    name = 'Distance from Alpha Centauri to Proxima Centauri'
    base_scale = 15
    color = (0, 255, 0)
    radius = 1.8


class DistanceFromSedna(Distance):
    """item sprite."""

    name = 'Distance from Sedna to Sun'
    base_scale = 12 + 2
    color = (0, 255, 0)
    radius = 1.40


class DistanceFromHaleBopp(Distance):
    """item sprite."""

    name = 'Distance from Comet Hale-Bopp to Sun'
    base_scale = 12 + 1
    color = (0, 255, 0)
    radius = 5.3
