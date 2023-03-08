"""Galaxy."""

from ..circular import Circular


def color(value):
    return int(value /2), value, value


class SmallGalaxy(Circular):
    """Item sprite."""
    base_scale = 18 + 2
    color = color(192)
    label_color = (0, 0, 0)


GALAXIES = [
    SmallGalaxy('Whirlpool Galaxy', size=7.20),
    SmallGalaxy('Triangulum Galaxy', size=5.70),
    SmallGalaxy('Sombrero Galaxy', size=4.60),
    SmallGalaxy('NGC 3310', size=2.90),
    SmallGalaxy('Large Magellanic Cloud', size=1.30),
]
