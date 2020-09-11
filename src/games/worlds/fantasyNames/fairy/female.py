from games.worlds.database import genders
from .base import BaseNameFactory


class FemaleNameFactory(BaseNameFactory):
    gender = genders.FEMALE

    @property
    def name(self):
        return f'{self.names_female} {self.names_family}{self.names_family_2}'
