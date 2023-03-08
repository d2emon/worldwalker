"""Galaxy."""

from ..circular import Circular


def color(value):
    return int(value /2), value, value


class Galaxy(Circular):
    """Item sprite."""
    base_scale = 21
    color = color(255)
    label_color = (0, 0, 0)


GALAXIES = [
    Galaxy('IC 1101', size=5.0),
    Galaxy('Toadpole Galaxy', size=4.0),
    Galaxy('NGC 4889', size=2.4),
    Galaxy('NGC 1232', size=1.9),
    Galaxy('Pinwheel Galaxy', size=1.7),
    Galaxy('Andromeda Galaxy', size=1.4),
    Galaxy('Cartwheel Galaxy', size=1.2),
    Galaxy('Virgo A Galaxy', size=1.2),
    Galaxy('Milky Way Galaxy', size=1.2),
    Galaxy('Canis Major Dwarf Galaxy', size=1.0),
]
