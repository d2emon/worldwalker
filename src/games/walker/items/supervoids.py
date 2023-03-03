"""Eridanus supervoid."""

from .circular import Circular


class Supervoid(Circular):
    def __init__(self, name, size=None):
        super().__init__(
            name,
            scale=24,
            size=size,
            color=(9, 9, 9),
        )


SUPERVOIDS = [
    Supervoid('Eridanus Supervoid', size=7.1),
]
