import random
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


class ComplexNameGenerator:
    def __init__(self, name_generators):
        self.__generator_id = None
        self.__cache = dict()
        self.name_generators = name_generators

    def get_cached(self, name_generator):
        cached = self.__cache.get(name_generator)
        if cached:
            return cached

        if isinstance(name_generator, type):
            cached = name_generator()
        else:
            cached = name_generator

        self.__cache[name_generator] = cached
        return cached

    @property
    def generator_ids(self):
        return range(len(self.name_generators))

    @property
    def generator_id(self):
        if self.__generator_id is not None:
            return self.__generator_id
        return random.choice(self.generator_ids)

    @generator_id.setter
    def generator_id(self, value):
        self.__generator_id = value

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.name_generators) <= 0:
            return None

        name_generator = self.get_cached(self.name_generators[self.generator_id])
        return next(name_generator)


class GenderedNameGenerator(ComplexNameGenerator):
    def __init__(self, name_generators=None):
        super().__init__(name_generators or dict())

    @property
    def generator_ids(self):
        return list(self.name_generators.keys())

    @property
    def genders(self):
        return self.generator_ids

    @property
    def gender(self):
        return self.generator_id

    @gender.setter
    def gender(self, value):
        self.generator_id = value


def build_name_generator(*args):
    name_generators = []
    for arg in args:
        name_generator, min_id, max_id = arg
        for _ in range(min_id, max_id):
            name_generators.append(name_generator)
    return ComplexNameGenerator(name_generators)

