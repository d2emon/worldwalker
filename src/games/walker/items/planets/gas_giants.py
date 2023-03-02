"""Planets."""

from ..circular import Circular


class GasGiant(Circular):
    """Item sprite."""
    base_scale = 6 + 2
    color = (0, 128, 255)
    label_color = (255, 255, 255)


class TrES4b(GasGiant):
    """Item sprite."""
    name = 'TrES-4b'
    base_size = 2.60


class Jupiter(GasGiant):
    """Item sprite."""
    name = 'Jupiter'
    base_size = 1.40


class Saturn(GasGiant):
    """Item sprite."""
    name = 'Saturn'
    base_size = 1.20


class Uranus(GasGiant):
    """Item sprite."""
    name = 'Uranus'
    base_scale = 6 + 1
    base_size = 5.10


class Neptune(GasGiant):
    """Item sprite."""
    name = 'Neptune'
    base_scale = 6 + 1
    base_size = 4.90


class Minecraft(GasGiant):
    """Item sprite."""
    name = 'Minecraft'
    base_scale = 6 + 1
    base_size = 6.40
    color = (0, 255, 0)
