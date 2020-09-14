from .base import BaseNamedFactory
from .swear import test_swear


class NamedFactory(BaseNamedFactory):
    def __init__(self, providers=None):
        self.providers = providers
        self.data = {}
        self.reset()

    def reset(self):
        self.data = {key: value.ready() for key, value in self.providers.items()}

    def name_parts(self):
        return {part: next(self.data[part]) for part in self.data.keys()}

    @classmethod
    def name(cls, **kwargs):
        return ''

    @property
    def factory(self):
        while True:
            self.reset()
            name = str(self.name(**self.name_parts()))
            if test_swear(name):
                yield name
