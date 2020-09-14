from genelib.fng.namegen import NamedFactory, ComplexFactory, PercentsFactory
from genelib.fng.name_factory import NameFactory as BaseNameFactory
from ..database.provider import group_providers_from_list


class BaseWorldDestroyerNameGenerator(NamedFactory):
    NAME_V1 = 1
    NAME_V2 = 2
    NAME_V3 = 3
    NAME_V4 = 4
    name_type = NAME_V1

    def __init__(self, providers=None):
        super().__init__(providers or group_providers_from_list('world-destroyer', [
            'nm1',
            'nm2',  # nm2.splice(rnd2, 1)
            'nm3',  # nm3.splice(rnd, 1)
            'nm4',
        ]))


class WorldDestroyerNameGenerator1(BaseWorldDestroyerNameGenerator):
    name_type = BaseWorldDestroyerNameGenerator.NAME_V1
    template = "The {nm1} {nm2}"


class WorldDestroyerNameGenerator2(BaseWorldDestroyerNameGenerator):
    name_type = BaseWorldDestroyerNameGenerator.NAME_V2
    template = "{nm2} of {nm4}"


class WorldDestroyerNameGenerator3(BaseWorldDestroyerNameGenerator):
    name_type = BaseWorldDestroyerNameGenerator.NAME_V3
    template = "The {nm3} of {nm2}"


class WorldDestroyerNameGenerator4(BaseWorldDestroyerNameGenerator):
    name_type = BaseWorldDestroyerNameGenerator.NAME_V4
    template = "The {nm3} {nm1} {nm2}"


class NameFactory(BaseNameFactory):
    factory = PercentsFactory({
        30: WorldDestroyerNameGenerator1,
        60: WorldDestroyerNameGenerator2,
        80: WorldDestroyerNameGenerator3,
        100: WorldDestroyerNameGenerator4,
    })
