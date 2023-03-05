"""Eridanus supervoid."""

from .circular import Circular


class Supervoid(Circular):
    def __init__(self, name, size=7.0, **kwargs):
        super().__init__(
            name,
            scale=24,
            size=size,
            color=(0, 0, 0, 192),
            **kwargs,
        )


SUPERVOIDS = [
    Supervoid('Eridanus Supervoid', size=7.1, visible=False),
]
