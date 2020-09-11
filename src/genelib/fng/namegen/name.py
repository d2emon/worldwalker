from .. import genders
from .swear import test_swear


class NameFactory:
    default_providers = {}
    gender = genders.NEUTRAL
    name_type = 0

    used_parts = []

    def __init__(self, providers=None):
        self.providers = providers or self.default_providers
        self.data = self.__ready_providers()

    def __iter__(self):
        return self

    def __next__(self):
        self.reset()
        name = self.name
        return name if test_swear(name) else next(self)

    def __ready_providers(self):
        return {key: value.ready() for key, value in self.providers.items()}

    def reset(self):
        self.data = self.__ready_providers()

    def name_parts(self):
        return {part: next(self.data[part]) for part in self.used_parts}

    @property
    def name(self):
        return ''
