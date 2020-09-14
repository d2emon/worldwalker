from genelib.fng.namegen import NamedFactory, ComplexFactory, PercentsFactory
from genelib.fng.name_factory import NameFactory as BaseNameFactory
from ..database.provider import group_providers_from_list


class BaseWorldDefenderNameGenerator(NamedFactory):
    NAME_V1 = 1
    NAME_V2 = 2
    NAME_V3 = 3
    NAME_V4 = 4
    name_type = NAME_V1

    def __init__(self, providers=None):
        super().__init__(providers or group_providers_from_list('world-defender', [
            'nm1',
            'nm2',  # nm2.splice(rnd2, 1)
            'nm3',  # nm3.splice(rnd, 1)
            'nm4',
        ]))


class WorldDefenderNameGenerator1(BaseWorldDefenderNameGenerator):
    name_type = BaseWorldDefenderNameGenerator.NAME_V1
    template = "The {nm1} {nm3}"


class WorldDefenderNameGenerator2(BaseWorldDefenderNameGenerator):
    name_type = BaseWorldDefenderNameGenerator.NAME_V2
    template = "{nm2} of {nm4}"


class WorldDefenderNameGenerator3(BaseWorldDefenderNameGenerator):
    name_type = BaseWorldDefenderNameGenerator.NAME_V3
    template = "The {nm3} of {nm2}"


class WorldDefenderNameGenerator4(BaseWorldDefenderNameGenerator):
    name_type = BaseWorldDefenderNameGenerator.NAME_V4
    template = "The {nm3} {nm1} {nm2}"


class NameFactory(BaseNameFactory):
    factory = PercentsFactory({
        30: WorldDefenderNameGenerator1,
        60: WorldDefenderNameGenerator2,
        80: WorldDefenderNameGenerator3,
        100: WorldDefenderNameGenerator4,
    })
