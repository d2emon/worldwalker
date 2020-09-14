from . import genders
from .swear import test_swear


class Name:
    def __init__(self, name='', gender=genders.NEUTRAL, **kwargs):
        self.__name = name
        self.gender = gender
        self.values = {**kwargs}

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    def __str__(self):
        return str(self.name)

    def test_swear(self):
        return test_swear(self.name)
