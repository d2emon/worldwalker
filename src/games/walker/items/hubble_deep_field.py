"""Hubble Deep Field sprite."""

from .distance import Distance


class HubbleDeepField(Distance):
    """item sprite."""

    name = 'Hubble Deep Field'
    base_scale = 24 + 2
    radius = 1.27
    color = (0, 255, 0)
