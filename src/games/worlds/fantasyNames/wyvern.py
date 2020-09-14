from genelib.fng import genders
from genelib.fng.namegen import GenderedFactory, ComplexFactory, PercentsFactory
from genelib.fng.name_factory import GenderedNameFactory
from ..database.provider import group_providers_from_list, group_providers_from_dict
from ..genelib import SyllablicGenerator, unique_with


class BaseWyvernNameGenerator(SyllablicGenerator):
    NAME_V1 = 1
    NAME_V2 = 2
    name_type = NAME_V1
    templates = {
        NAME_V1: (1, 2, 3, 4, 5),
        NAME_V2: (1, 2, 3, 4, 6, 7, 5),
    }

    def __init__(self, providers=None):
        super().__init__(providers or group_providers_from_list('wyvern', [
            'nm1',
            'nm2',
            'nm3',
            'nm4',
            'nm5',
            'nm6',
            'nm7',
            'nm8',
            'nm9',
            'nm10',
            'nm11',
            'nm12',
            'nm13',
            'nm14',
            'nm15',
        ]))

    @classmethod
    def template(cls):
        return cls.templates[cls.name_type]

    def name_rules(self):
        return {
            3: unique_with(1),
            5: unique_with(3),
            6: unique_with(3),
        }


class WyvernNameRulesV1(BaseWyvernNameGenerator):
    name_type = BaseWyvernNameGenerator.NAME_V1


class WyvernNameRulesV2(WyvernNameRulesV1):
    name_type = BaseWyvernNameGenerator.NAME_V2


class BaseMaleWyvernNameGenerator(BaseWyvernNameGenerator):
    gender = genders.MALE
    syllable_providers = group_providers_from_dict('wyvern', {
        1: 'nm1',
        2: 'nm2',
        3: 'nm3',
        4: 'nm2',
        5: 'nm5',

        6: 'nm4',
        7: 'nm2',
    })


class BaseFemaleWyvernNameGenerator(BaseWyvernNameGenerator):
    gender = genders.FEMALE
    syllable_providers = group_providers_from_dict('wyvern', {
        1: 'nm6',
        2: 'nm7',
        3: 'nm8',
        4: 'nm7',
        5: 'nm10',

        6: 'nm9',
        7: 'nm7',
    })


class BaseNeutralWyvernNameGenerator(BaseWyvernNameGenerator):
    gender = genders.NEUTRAL
    syllable_providers = group_providers_from_dict('wyvern', {
        1: 'nm11',
        2: 'nm12',
        3: 'nm13',
        4: 'nm12',
        5: 'nm15',

        6: 'nm14',
        7: 'nm12',
    })


class MaleWyvernNameGenerator1(WyvernNameRulesV1, BaseMaleWyvernNameGenerator):
    pass


class MaleWyvernNameGenerator2(WyvernNameRulesV2, BaseMaleWyvernNameGenerator):
    pass


class FemaleWyvernNameGenerator1(WyvernNameRulesV1, BaseFemaleWyvernNameGenerator):
    pass


class FemaleWyvernNameGenerator2(WyvernNameRulesV2, BaseFemaleWyvernNameGenerator):
    pass


class WyvernNameGenerator1(WyvernNameRulesV1, BaseNeutralWyvernNameGenerator):
    pass


class WyvernNameGenerator2(WyvernNameRulesV2, BaseNeutralWyvernNameGenerator):
    pass


class NameFactory(GenderedNameFactory):
    factory = GenderedFactory(
        male=PercentsFactory({
            70: MaleWyvernNameGenerator1,
            100: MaleWyvernNameGenerator2,
        }),
        female=PercentsFactory({
            70: FemaleWyvernNameGenerator1,
            100: FemaleWyvernNameGenerator2,
        }),
        neutral=PercentsFactory({
            70: WyvernNameGenerator1,
            100: WyvernNameGenerator2,
        }),
    )
