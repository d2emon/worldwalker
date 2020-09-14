from genelib.fng import genders
from .base import BaseNameFactory


class MaleNameFactory(BaseNameFactory):
    gender = genders.MALE

    @property
    def name(self):
        return f'{self.nm3} {self.nm2}'
