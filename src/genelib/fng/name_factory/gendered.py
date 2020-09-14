from .name import NameFactory
from ..namegen import GenderedFactory


class GenderedNameFactory(NameFactory):
    factory = GenderedFactory()

    @classmethod
    def next(cls, gender, *args, **kwargs):
        cls.factory.gender = gender
        return next(cls.factory)
