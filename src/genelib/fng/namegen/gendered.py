from .. import genders
from .complex import ComplexFactory


class GenderedFactory(ComplexFactory):
    def __init__(self, *args, male=None, female=None, neutral=None, **kwargs):
        super().__init__(*args, **kwargs)
        if male:
            self.factories[genders.MALE] = male
        if female:
            self.factories[genders.MALE] = female
        if neutral:
            self.factories[genders.MALE] = neutral

    @property
    def genders(self):
        return self.factories.keys()

    @property
    def gender(self):
        return self.factory_id

    @gender.setter
    def gender(self, value):
        self.factory_id = value
