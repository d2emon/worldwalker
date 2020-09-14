from genelib.fng import genders
from genelib.fng.namegen import GenderedFactory, NamedFactory
from genelib.fng.name_factory import GenderedNameFactory
from games.worlds.database.provider import group_providers_from_list
from .name import WitchName


class WitchNameFactory(GenderedNameFactory):
    class Base(NamedFactory):
        def __init__(self, providers=None):
            super().__init__(providers or group_providers_from_list('witch', [
                'nm1',
                'nm2',
                'nm3',
            ]))

    class Male(Base):
        def name(self, **kwargs):
            return WitchName(
                gender=genders.MALE,
                **kwargs,
            )

    class Female(Base):
        def name(self, **kwargs):
            return WitchName(
                gender=genders.FEMALE,
                **kwargs,
            )

    factory = GenderedFactory(
        male=Male,
        female=Female,
    )
