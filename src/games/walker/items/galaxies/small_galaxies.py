"""Galaxy."""

from ..circular import Circular


def color(value):
    return int(value /2), value, value


class SmallGalaxy(Circular):
    """Item sprite."""
    base_scale = 18 + 2
    color = color(192)
    label_color = (0, 0, 0)


class Whirlpool(SmallGalaxy):
    """Item sprite."""
    name = 'Whirlpool Galaxy'
    base_size = 7.20
    color = color(184)


class Triangulum(SmallGalaxy):
    """Item sprite."""
    name = 'Triangulum Galaxy'
    base_size = 5.70
    color = color(176)


class Sombrero(SmallGalaxy):
    """Item sprite."""
    name = 'Sombrero Galaxy'
    base_size = 4.60
    color = color(168)


class NGC3310(SmallGalaxy):
    """Item sprite."""
    name = 'NGC 3310'
    base_size = 2.90
    color = color(160)


class LargeMagellanicCloud(SmallGalaxy):
    """Item sprite."""
    name = 'Large Magellanic Cloud'
    base_size = 1.30
    color = color(152)


GALAXIES = [
    SmallGalaxy('Whirlpool Galaxy', size=7.20),
    SmallGalaxy('Triangulum Galaxy', size=5.70),
    SmallGalaxy('Sombrero Galaxy', size=4.60),
    SmallGalaxy('NGC 3310', size=2.90),
    SmallGalaxy('Large Magellanic Cloud', size=1.30),
]
