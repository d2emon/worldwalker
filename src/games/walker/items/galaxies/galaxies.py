"""Galaxy."""

from ..circular import Circular


def color(value):
    return int(value /2), value, value


class Galaxy(Circular):
    """Item sprite."""
    base_scale = 21
    color = color(255)
    label_color = (0, 0, 0)


class IC1101(Galaxy):
    """Item sprite."""
    name = 'IC 1101'
    base_size = 5.0
    color = color(255)


class Toadpole(Galaxy):
    """Item sprite."""
    name = 'Toadpole Galaxy'
    base_size = 4.0
    color = color(252)


class NGC4889(Galaxy):
    """Item sprite."""
    name = 'NGC 4889'
    base_size = 2.4
    color = color(248)


class NGC1232(Galaxy):
    """Item sprite."""
    name = 'NGC 1232'
    base_size = 1.9
    color = color(244)


class Pinwheel(Galaxy):
    """Item sprite."""
    name = 'Pinwheel Galaxy'
    base_size = 1.7
    color = color(240)


class Andromeda(Galaxy):
    """Item sprite."""
    name = 'Andromeda Galaxy'
    base_size = 1.4
    color = color(236)


class Cartwheel(Galaxy):
    """Item sprite."""
    name = 'Cartwheel Galaxy'
    base_size = 1.2
    color = color(232)


class VirgoA(Galaxy):
    """Item sprite."""
    name = 'Virgo A Galaxy'
    base_size = 1.2
    color = color(228)


class MilkyWay(Galaxy):
    """Item sprite."""
    name = 'Milky Way Galaxy'
    base_size = 1.2
    color = color(224)


class CanisMajor(Galaxy):
    """Item sprite."""
    name = 'Canis Major Dwarf Galaxy'
    base_size = 1.0
    color = color(220)
