from games.worlds.database import genders
from .base import BaseNameFactory


class MaleNameFactory(BaseNameFactory):
    gender = genders.MALE

    @property
    def name(self):
        return f'{self.names_male} {self.names_family}{self.names_family_2}'
