"""Galaxy."""

from ..circular import Circular


def color(value):
    return int(value /2), value, value


class Galaxy(Circular):
    """Item sprite."""
    base_scale = 18 + 1
    color = color(128)
    label_color = (0, 0, 0)


class Sagittarius(Galaxy):
    """Item sprite."""
    name = 'Sagittarius Dwarf Galaxy'
    base_size = 9.4
    color = color(120)


class SmallMagellanicCloud(Galaxy):
    """Item sprite."""
    name = 'Small Magellanic Cloud'
    base_size = 6.6
    color = color(112)


class CanisVenatici(Galaxy):
    """Item sprite."""
    name = 'Canis Venatici Dwarf Galaxy'
    base_size = 3.4
    color = color(106)


class Leo2(Galaxy):
    """Item sprite."""
    name = 'Leo II Dwarf Galaxy'
    base_size = 2.2
    color = color(98)
