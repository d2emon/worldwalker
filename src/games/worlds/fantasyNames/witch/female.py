from genelib.fng import genders
from .base import BaseNameFactory


class FemaleNameFactory(BaseNameFactory):
    gender = genders.FEMALE
    template = "{nm1} {nm2}"

    @property
    def name(self):
        return f'{self.nm1} {self.nm2}'
