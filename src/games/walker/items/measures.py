"""Gigaparsec sprite."""

from .circular import Circular


MEASURES = [
    Circular('Gigaparsec', scale=24 + 1, size=3.3, color=(128, 128, 128), border=2, visible=False),
    Circular('Megaparsec', scale=21 + 1, size=3.3, color=(128, 128, 128), border=2),
    Circular('Kiloparsec', scale=18 + 1, size=3.3, color=(128, 128, 128), border=2),
    Circular('Parsec', scale=15 + 1, size=3.1, color=(128, 128, 128), border=2),
]
