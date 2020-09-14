from .. import genders
from .complex import ComplexFactory


class GenderedFactory(ComplexFactory):
    def __init__(self, *args, male=None, female=None, neutral=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.factories[genders.MALE] = male
        self.factories[genders.FEMALE] = female
        self.factories[genders.NEUTRAL] = neutral

    @property
    def genders(self):
        return self.factories.keys()

    @property
    def gender(self):
        return self.factory_id

    @gender.setter
    def gender(self, value):
        self.factory_id = value
