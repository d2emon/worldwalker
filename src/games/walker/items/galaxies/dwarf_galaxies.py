"""Galaxy."""

from ..circular import Circular


def color(value):
    return int(value /2), value, value


class DwarfGalaxy(Circular):
    """Item sprite."""
    base_scale = 18 + 1
    color = color(128)
    label_color = (0, 0, 0)


class Sagittarius(DwarfGalaxy):
    """Item sprite."""
    name = 'Sagittarius Dwarf Galaxy'
    base_size = 9.4
    color = color(120)


class SmallMagellanicCloud(DwarfGalaxy):
    """Item sprite."""
    name = 'Small Magellanic Cloud'
    base_size = 6.6
    color = color(112)


class CanisVenatici(DwarfGalaxy):
    """Item sprite."""
    name = 'Canis Venatici Dwarf Galaxy'
    base_size = 3.4
    color = color(106)


class Leo2(DwarfGalaxy):
    """Item sprite."""
    name = 'Leo II Dwarf Galaxy'
    base_size = 2.2
    color = color(98)




GALAXIES = [
    DwarfGalaxy('Sagittarius Dwarf Galaxy', size=9.4),
    DwarfGalaxy('Small Magellanic Cloud', size=6.6),
    DwarfGalaxy('Canis Venatici Dwarf Galaxy', size=3.4),
    DwarfGalaxy('Leo II Dwarf Galaxy', size=2.2),
]
