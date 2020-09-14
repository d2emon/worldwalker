from genelib.fng import genders
from genelib.fng.namegen import GenderedFactory, NamedFactory
from genelib.fng.name_factory import GenderedNameFactory
from games.worlds.database.provider import group_providers_from_list


class FairyNameFactory(GenderedNameFactory):
    class Base(NamedFactory):
        def __init__(self, providers=None):
            super().__init__(providers or group_providers_from_list('fairy', [
                'names_male',
                'names_female',
                'names_family',
                'names_family_2',
            ]))

    class Male(Base):
        gender = genders.MALE

        @classmethod
        def name(cls, names_male='', names_family='', names_family_2='', **kwargs):
            return f'{names_male} {names_family}{names_family_2}'

    class Female(Base):
        gender = genders.FEMALE

        @classmethod
        def name(cls, names_female='', names_family='', names_family_2='', **kwargs):
            return f'{names_female} {names_family}{names_family_2}'

    factory = GenderedFactory(
        male=Male,
        female=Female,
    )
