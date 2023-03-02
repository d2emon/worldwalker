"""Structures."""

from ..circular import Circular


class Mountain(Circular):
    """Item sprite."""
    base_scale = 3
    color = (128, 128, 128)
    label_color = (255, 255, 255)


class Everest(Mountain):
    """Item sprite."""
    name = 'Everest'
    base_size = 8.8
