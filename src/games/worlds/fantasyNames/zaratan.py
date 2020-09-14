from genelib.fng.namegen import ComplexFactory, PercentsFactory
from genelib.fng.name_factory import NameFactory as BaseNameFactory
from ..database.provider import group_providers_from_list, group_providers_from_dict
from games.worlds.genelib import SyllablicGenerator, unique_with


class BaseZaratanNameGenerator(SyllablicGenerator):
    NAME_V1 = 1
    NAME_V2 = 2
    name_type = NAME_V1
    syllable_providers = group_providers_from_dict('zaratan', {
        1: 'nm1',
        2: 'nm2',
        3: 'nm3',
        4: 'nm4',
        5: 'nm6',

        6: 'nm5',
        7: 'nm2',
    })
    templates = {
        NAME_V1: (1, 2, 3, 4, 5),
        NAME_V2: (1, 2, 3, 4, 6, 7, 5),
    }

    def __init__(self, providers=None):
        super().__init__(providers or group_providers_from_list('zaratan', [
            'nm1',
            'nm2',
            'nm3',
            'nm4',
            'nm5',
            'nm6',
        ]))

    @classmethod
    def template(cls):
        return cls.templates[cls.name_type]

    def name_rules(self):
        return {
            3: unique_with(1, 5),
        }


class ZaratanNameGenerator1(BaseZaratanNameGenerator):
    pass


class ZaratanNameGenerator2(BaseZaratanNameGenerator):
    def name_rules(self):
        rules = super().name_rules()
        rules[5] = unique_with(2, 4)
        return rules


class NameFactory(BaseNameFactory):
    factory = PercentsFactory({
        50: ZaratanNameGenerator1,
        100: ZaratanNameGenerator2,
    })
