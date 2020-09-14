from .base import BaseNamedFactory
from ..name import Name


class NamedFactory(BaseNamedFactory):
    def __init__(self, providers=None):
        self.providers = providers
        self.data = {}
        self.reset()

    def reset(self):
        self.data = {key: value.ready() for key, value in self.providers.items()}

    def name_parts(self):
        return {part: next(self.data[part]) for part in self.data.keys()}

    def name(self, **kwargs):
        return Name(
            name='',
            gender=self.gender,
            **kwargs,
        )

    @property
    def factory(self):
        while True:
            self.reset()
            name = self.name(**self.name_parts())
            if name.test_swear():
                yield name
