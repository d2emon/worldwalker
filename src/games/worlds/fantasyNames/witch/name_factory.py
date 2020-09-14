from genelib.fng import genders
from genelib.fng.namegen import GenderedFactory, NamedFactory
from genelib.fng.name_factory import GenderedNameFactory
from games.worlds.database.provider import group_providers_from_list


class WitchNameFactory(GenderedNameFactory):
    class Base(NamedFactory):
        def __init__(self, providers=None):
            super().__init__(providers or group_providers_from_list('witch', [
                'nm1',
                'nm2',
                'nm3',
            ]))

    class Male(Base):
        gender = genders.MALE

        @classmethod
        def name(cls, nm2='', nm3='', **kwargs):
            return f'{nm3} {nm2}'

    class Female(Base):
        gender = genders.FEMALE

        @classmethod
        def name(cls, nm1='', nm2='', **kwargs):
            return f'{nm1} {nm2}'

    factory = GenderedFactory(
        male=Male,
        female=Female,
    )
