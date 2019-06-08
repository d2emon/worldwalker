from .base_player import BasePlayer

"""
"""


class User(BasePlayer):
    def __init__(self, name):
        self.__name = name

        self.__in_setup = False
        self.__position = -1
        self.__location_id = 0

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def location_id(self):
        return self.__location_id

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def strength(self):
        raise NotImplementedError()

    @property
    def visible(self):
        raise NotImplementedError()

    @property
    def flags(self):
        raise NotImplementedError()

    @property
    def level(self):
        raise NotImplementedError()

    @property
    def weapon(self):
        raise NotImplementedError()

    @property
    def helping(self):
        raise NotImplementedError()

    @property
    def sex(self):
        raise NotImplementedError()

    @property
    def is_mobile(self):
        raise NotImplementedError()

    def dumpstuff(self, location):
        pass
