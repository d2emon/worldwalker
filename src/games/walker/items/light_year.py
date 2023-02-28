"""Light Year sprite."""

from .circular import Circular


class LightYear(Circular):
    """item sprite."""

    name = 'LightYear'
    base_scale = 15 + 1
    base_size = 1.0
    color = (128, 128, 128)
    border = 2


class LightDay(Circular):
    """item sprite."""

    name = 'LightYear'
    base_scale = 12 + 1
    base_size = 2.6
    color = (128, 128, 128)
    border = 2
