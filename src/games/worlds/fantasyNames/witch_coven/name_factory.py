from genelib.fng.namegen import NamedFactory, PercentsFactory
from genelib.fng.name_factory import NameFactory
from games.worlds.database.provider import group_providers_from_list
from .name import WitchCovenName


class Base(NamedFactory):
    NAME_V1 = 1
    NAME_V2 = 2
    name_type = NAME_V1

    def __init__(self, providers=None):
        super().__init__(providers or group_providers_from_list('witch-coven', [
            'nm1',  # nm1.splice(rnd, 1)
            'nm2',  # nm2.splice(rnd, 1)
            'nm3',
        ]))

    def name(self, **kwargs):
        return WitchCovenName(
            name_type=self.name_type,
            **kwargs,
        )


class Name1(Base):
    name_type = 1


class Name2(Base):
    name_type = 2


class WitchCovenNameFactory(NameFactory):
    factory = PercentsFactory({
        50: Name1,
        100: Name2,
    })
