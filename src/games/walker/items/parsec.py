"""Parsec sprite."""

from .circular import Circular


class Parsec(Circular):
    """item sprite."""

    name = 'Parsec'
    base_scale = 15 + 1
    base_size = 3.1
    color = (128, 128, 128)
    border = 2


class Gigaparsec(Circular):
    """item sprite."""

    name = 'Gigaparsec'
    base_scale = 24 + 1
    base_size = 3.3
    color = (128, 128, 128)
    border = 2
