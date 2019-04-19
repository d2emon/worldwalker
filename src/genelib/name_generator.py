import random
from .swear import test_swear
from .data_provider import DataProvider
from .genders import GENDER_NEUTRAL


class NameGenerator:
    default_providers = dict()
    gender = GENDER_NEUTRAL
    name_type = 0

    template = ""
    used_parts = []

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

    def name_parts(self):
        return {part: next(self.data[part]) for part in self.used_parts}

    def name(self):
        return self.template.format(**self.name_parts())


class ListNameGenerator(NameGenerator):
    default_provider = DataProvider([])

    template = "{provider}"
    used_parts = ["provider"]

    def __init__(self, provider=None):
        provider = provider or self.default_provider
        super().__init__({'provider': provider})


class SyllableGenerator(ListNameGenerator):
    def __init__(self, provider):
        super().__init__(provider)

    def name(self):
        return next(self.data['provider'])


class SyllablicGenerator(NameGenerator):
    syllable_providers = dict()
    GLUE = ""

    def __init__(self, providers=None):
        super().__init__(providers)
        self.syllable_generators = self.prepare_syllable_generators()

    def template(self):
        return ()

    def prepare_syllable_generators(self):
        return {
            syllable_id: SyllableGenerator(syllable_provider)
            for syllable_id, syllable_provider in self.syllable_providers.items()
        }

    def name_rules(self):
        return dict()

    def rules(self, syllables):
        for syllable_id in syllables.keys():
            rule = self.name_rules().get(syllable_id)
            if rule is None:
                continue
            while not rule(syllables[syllable_id], syllables):
                print(rule, syllables[syllable_id])
                syllables[syllable_id] = next(self.syllable_generators[syllable_id])
        return syllables

    def syllables(self):
        return self.rules({
            syllable_id: next(syllable)
            for syllable_id, syllable in self.syllable_generators.items()
        })

    @classmethod
    def join_syllables(cls, syllables, *args):
        return cls.GLUE.join(syllables)

    @classmethod
    def from_syllables(cls, syllables, order):
        return cls.GLUE.join([
            str(syllables[syllable_id]) for syllable_id in order
        ])

    def name(self):
        # syllables = self.syllables()
        # return self.join_syllables(syllables)
        return self.from_syllables(self.syllables(), self.template())\
               + ".{}".format(self.name_type) + ".{}".format(self.gender)


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

