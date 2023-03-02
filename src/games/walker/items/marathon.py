"""Marathon sprite."""

from .circular import Circular


class Marathon(Circular):
    """item sprite."""

    name = 'Marathon'
    base_scale = 3 + 1
    base_size = 4.22
    color = (128, 128, 128)
    border = 2
