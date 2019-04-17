from .swear import test_swear
from .data_provider import DataProvider


class NameGenerator:
    default_providers = dict()

    def __init__(self, providers=None):
        self.providers = providers or self.default_providers
        self.data = self.__ready_providers()

    def __iter__(self):
        return self

    def __next__(self):
        self.reset()
        name = self.name()
        valid = test_swear(str(name))
        if not valid:
            return next(self)
        return name

    def __ready_providers(self):
        return {key: value.ready() for key, value in self.providers.items()}

    def reset(self):
        self.data = self.__ready_providers()

    def name(self):
        return "Name"

    @classmethod
    def unique(cls, item, unique_with, data):
        while str(item) == str(unique_with):
            item = next(data)
        return item


class ListNameGenerator(NameGenerator):
    default_provider = DataProvider([])

    def __init__(self, provider=None):
        provider = provider or self.default_provider
        super().__init__({'provider': provider})

    def name(self):
        return next(self.data['provider'])


class SyllableGenerator(ListNameGenerator):
    def __init__(self, provider):
        super().__init__(provider)


class SyllablicGenerator(NameGenerator):
    syllable_providers = dict()
    GLUE = ""

    def __init__(self, providers=None):
        super().__init__(providers)
        self.syllable_generators = self.prepare_syllable_generators()

    def prepare_syllable_generators(self):
        return {
            syllable_id: SyllableGenerator(syllable_provider)
            for syllable_id, syllable_provider in self.syllable_providers.items()
        }

    def rules(self, syllables):
        return syllables

    def syllables(self):
        return self.rules({
            syllable_id: next(syllable)
            for syllable_id, syllable in self.syllable_generators.items()
        })

    @classmethod
    def join_syllables(cls, syllables, *args):
        return cls.GLUE.join(syllables)

    def name(self):
        syllables = self.syllables()
        return self.join_syllables(syllables)
