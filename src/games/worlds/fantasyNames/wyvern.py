from genelib.fng import genders
from genelib.fng.named import Gendered
from genelib.fng.namegen import GenderedFactory
from ..database.provider import group_providers_from_list, group_providers_from_dict
from ..genelib import SyllablicGenerator, build_name_generator, unique_with


class BaseWyvernNameGenerator(SyllablicGenerator):
    NAME_V1 = 1
    NAME_V2 = 2
    name_type = NAME_V1
    default_providers = group_providers_from_list('wyvern', [
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
    ])
    templates = {
        NAME_V1: (1, 2, 3, 4, 5),
        NAME_V2: (1, 2, 3, 4, 6, 7, 5),
    }

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


class Wyvern(Gendered):
    """
    Wyverns are creatures similar to dragons, except they only have 2 legs and usually a barbed tail. Wyverns usually
    also don't breathe fire either, but their bite is venemous. However, all these details vary from work of fiction to
    work of fiction.

    As far as names go, wyvern names tend to be far more vicious sounding than their dragon counterparts, perhaps
    because wyverns are often depicted as less intelligent and more animalistic and aggressive or perhaps for a
    different reason entirely. Either way I focused on these kinds of names in this generator. If you are looking for
    more melodic names the dragon name generator is a great place to start.
    """

    class NameFactory(Gendered.NameFactory):
        factory = GenderedFactory(
            male=build_name_generator(
                (MaleWyvernNameGenerator1, 0, 7),
                (MaleWyvernNameGenerator2, 7, 10),
            ),
            female=build_name_generator(
                (FemaleWyvernNameGenerator1, 0, 7),
                (FemaleWyvernNameGenerator2, 7, 10),
            ),
            neutral=build_name_generator(
                (WyvernNameGenerator1, 0, 7),
                (WyvernNameGenerator2, 7, 10),
            ),
        )
