import random
from ..namegen import GenderedFactory
from .named import Named


class Gendered(Named):
    class NameFactory(Named.NameFactory):
        factory = GenderedFactory()

        @classmethod
        def __name_factory(cls, gender):
            factories = cls.factory.get(gender) or [None]
            return random.choice(factories)

        @classmethod
        def next(cls, gender, *args, **kwargs):
            cls.factory.gender = gender
            return next(cls.factory)
