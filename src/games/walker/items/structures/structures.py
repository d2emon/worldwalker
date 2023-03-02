"""Structures."""

from ..square import Square


class Structure(Square):
    """Item sprite."""
    base_scale = 3
    color = (128, 128, 128)
    label_color = (255, 255, 255)


class GreatWallOfChina(Structure):
    """Item sprite."""
    name = 'Great Wall of China'
    base_scale = 6
    base_size = 2.9


class LHC(Structure):
    """Item sprite."""
    name = 'Large Hadron Collider'
    base_size = 8.6


class PalmJebelAli(Structure):
    """Item sprite."""
    name = 'Palm Jebel Ali'
    base_size = 8.0


class CentralPark(Structure):
    """Item sprite."""
    name = 'Central Park'
    base_size = 4.0
