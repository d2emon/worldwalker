from . import genders


class Name:
    def __init__(self, name='', gender=genders.NEUTRAL):
        self.name = name
        self.gender = gender

    def __str__(self):
        return str(self.name)
