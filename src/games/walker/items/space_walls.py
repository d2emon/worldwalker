"""Hercules-Corona Borealis Great Wall."""

from .square import Square


class Wall(Square):
    def __init__(self, name, size=9.0, *args, **kwargs):
        super().__init__(
            name,
            scale=24 + 1,
            size=size,
            color=(0, 255, 0),
            *args,
            **kwargs,
        )


WALLS = [
    Wall('Hercules-Corona Borealis Great Wall', size=9.0, visible=False),
]
