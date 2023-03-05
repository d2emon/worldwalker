"""Hubble Deep Field sprite."""

from .distance import Distance


DISTANCES = [
    Distance('Hubble Deep Field', scale=24 + 2, size=1.27, color=(0, 255, 0), visible=False),
    Distance('Distance to Great Attractor', scale=24, size=1.9, color=(0, 255, 0), visible=False),
    Distance('Distance to the Shapley Superclaster', scale=21 + 2, size=3.20, color=(0, 255, 0)),
]
