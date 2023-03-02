"""Structures."""

from ..circular import Circular


class Structure(Circular):
    """Item sprite."""
    base_scale = 3 + 2
    color = (128, 128, 128)
    label_color = (255, 255, 255)


class GreatBarrierReef(Structure):
    """Item sprite."""
    name = 'Great Barrier Reef'
    base_scale = 6
    base_size = 2.6


class GrandCanion(Structure):
    """Item sprite."""
    name = 'Grand Canion'
    base_size = 2.6


class MarianaTrench(Structure):
    """Item sprite."""
    name = 'Mariana Trench'
    base_size = 1.09
