import random
from .name_generator import NameGenerator


class Named:
    name_generators = [NameGenerator()]

    def __init__(self, name=''):
        self.name = name

    def __str__(self):
        return self.name

    @classmethod
    def name_generator(cls, *args):
        return random.choice(cls.name_generators)

    @classmethod
    def generate(cls, *args):
        return str(next(cls.name_generator(*args))).title()


class Gendered(Named):
    name_generators = dict()

    @classmethod
    def name_generator(cls, gender, *args):
        name_generators = cls.name_generators.get(gender)
        if name_generators is None:
            return None
        return random.choice(name_generators)
