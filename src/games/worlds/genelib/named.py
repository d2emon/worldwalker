import random
from .name_generator import ComplexNameGenerator, GenderedNameGenerator


class Named:
    name_generator = ComplexNameGenerator([])

    def __init__(self, name=''):
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    def generate_name(cls, *args):
        return str(next(cls.name_generator)).title()

    @classmethod
    def generate(cls, *args):
        return cls(cls.generate_name(*args))


class Gendered(Named):
    name_generator = GenderedNameGenerator()

    @classmethod
    def generate_name(cls, gender, *args):
        cls.name_generator.gender = gender
        return str(next(cls.name_generator)).title()

    @classmethod
    def name_generator(cls, gender, *args):
        name_generators = cls.name_generators.get(gender)
        if name_generators is None:
            return None
        return random.choice(name_generators)
