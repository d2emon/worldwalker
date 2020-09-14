from .. import genders
from ..name_factory import GenderedNameFactory
from .named import Named


class Gendered(Named):
    name_factory = GenderedNameFactory

    def __init__(self, name='', gender=genders.NEUTRAL, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.gender = gender
