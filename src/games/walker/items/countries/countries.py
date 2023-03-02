"""Countries."""

from ..square import Square


class Country(Square):
    """Item sprite."""
    base_scale = 3 + 2
    color = (0, 255, 0)
    label_color = (255, 255, 255)


class Usa(Country):
    """Item sprite."""
    name = 'USA'
    base_scale = 6
    base_size = 4.2


class California(Country):
    """Item sprite."""
    name = 'California'
    base_scale = 6
    base_size = 1.2


class Texas(Country):
    """Item sprite."""
    name = 'Texas'
    base_scale = 6
    base_size = 1.2


class Italy(Country):
    """Item sprite."""
    name = 'Italy'
    base_scale = 6
    base_size = 1.1


class WestVirginia(Country):
    """Item sprite."""
    name = 'West Virginia'
    base_size = 4.00


class Rwanda(Country):
    """Item sprite."""
    name = 'Rwanda'
    base_size = 2.40


class Brunei(Country):
    """Item sprite."""
    name = 'Brunei'
    base_size = 1.20


class RhodeIsland(Country):
    """Item sprite."""
    name = 'Rhode Island'
    base_scale = 3 + 1
    base_size = 7.5
