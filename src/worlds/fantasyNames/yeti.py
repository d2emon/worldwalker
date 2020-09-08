from ..database import get_data_providers, get_syllable_providers
from genelib import SyllablicGenerator, GenderedNameGenerator, Gendered, build_name_generator, unique_with
from genelib.genders import GENDER_NEUTRAL, GENDER_MALE, GENDER_FEMALE


class BaseYetiNameGenerator(SyllablicGenerator):
    NAME_V1 = 1
    NAME_V2 = 2
    NAME_V3 = 3
    name_type = NAME_V1
    default_providers = get_data_providers('yeti', [
        'nm1',
        'nm2',
        'nm3',
        'nm4',
        'nm4b',
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
    ])
    templates = {
        NAME_V1: (1, 2, 3, 4, 5),
        NAME_V2: (1, 2, 3, 4, 6, 7, 5),
        NAME_V3: (1, 2, 6, 7, 3, 4, 5),
    }

    min1 = 5
    min2 = 15

    @classmethod
    def template(cls):
        return cls.templates[cls.name_type]

    def name_rules(self):
        return {
            3: unique_with(1),
            5: unique_with(6),
            6: unique_with(3),
        }


class YetiNameRulesV1(BaseYetiNameGenerator):
    name_type = BaseYetiNameGenerator.NAME_V1

    def name_rules(self):
        def unique_3_5(syllable, syllables):
            if syllables[1].item_id >= self.min1:
                return True
            if syllable.item_id < self.min2:
                return False
            return str(syllable) != str(syllables[3])

        return {
            3: unique_with(1),
            5: unique_3_5,
        }


class YetiNameRulesV2(YetiNameRulesV1):
    name_type = BaseYetiNameGenerator.NAME_V2



class YetiNameRulesV3(YetiNameRulesV2):
    name_type = BaseYetiNameGenerator.NAME_V3


class BaseMaleYetiNameGenerator(BaseYetiNameGenerator):
    gender = GENDER_MALE
    syllable_providers = get_syllable_providers('yeti', {
        1: 'nm1',
        2: 'nm2',
        3: 'nm3',
        4: 'nm2',
        5: 'nm4',

        6: 'nm4b',
        7: 'nm2',
    })
    min1 = 5
    min2 = 2


class BaseFemaleYetiNameGenerator(BaseYetiNameGenerator):
    gender = GENDER_FEMALE
    syllable_providers = get_syllable_providers('yeti', {
        1: 'nm5',
        2: 'nm6',
        3: 'nm7',
        4: 'nm6',
        5: 'nm8',

        6: 'nm9',
        7: 'nm6',
    })


class BaseNeutralYetiNameGenerator(BaseYetiNameGenerator):
    gender = GENDER_NEUTRAL
    syllable_providers = get_syllable_providers('yeti', {
        1: 'nm10',
        2: 'nm11',
        3: 'nm12',
        4: 'nm11',
        5: 'nm13',

        6: 'nm14',
        7: 'nm11',
    })


class MaleYetiNameGenerator1(YetiNameRulesV1, BaseMaleYetiNameGenerator):
    pass


class MaleYetiNameGenerator2(YetiNameRulesV2, BaseMaleYetiNameGenerator):
    pass


class MaleYetiNameGenerator3(YetiNameRulesV3, BaseMaleYetiNameGenerator):
    pass


class FemaleYetiNameGenerator1(YetiNameRulesV1, BaseFemaleYetiNameGenerator):
    pass


class FemaleYetiNameGenerator2(YetiNameRulesV2, BaseFemaleYetiNameGenerator):
    pass


class FemaleYetiNameGenerator3(YetiNameRulesV3, BaseFemaleYetiNameGenerator):
    pass


class YetiNameGenerator1(YetiNameRulesV1, BaseNeutralYetiNameGenerator):
    pass


class YetiNameGenerator2(YetiNameRulesV2, BaseNeutralYetiNameGenerator):
    pass


class YetiNameGenerator3(YetiNameRulesV3, BaseNeutralYetiNameGenerator):
    pass


class Yeti(Gendered):
    """
    Yetis are ape-like humanoids who supposedly inhabit the Himalayan regions and are part of popular folklore,
    religion and mythologies. There are many variants in other regions too, like Bigfoot, the Yeren, the Yowie and so
    on.

    Yetis and similar creatures aren't often given personal names, in many cases because they're the only specimen
    believed to exist. This made creating a name generator a little tricky, but since these creatures do inhabit
    specific regions of the world I decided to take inspiration from those regions to create naming conventions. I
    focused primarily on the Himalayan regions, but also took some inspiration for some of the lesser known variants of
    'yeti' out there, like the before mentioned Yeren and Yowie.
    """
    MALE = GENDER_MALE
    FEMALE = GENDER_FEMALE
    NEUTRAL = GENDER_NEUTRAL

    name_generator = GenderedNameGenerator({
        MALE: build_name_generator(
            (MaleYetiNameGenerator1, 0, 6),
            (MaleYetiNameGenerator2, 6, 8),
            (MaleYetiNameGenerator3, 8, 10),
        ),
        FEMALE: build_name_generator(
            (FemaleYetiNameGenerator1, 0, 6),
            (FemaleYetiNameGenerator2, 6, 8),
            (FemaleYetiNameGenerator3, 8, 10),
        ),
        NEUTRAL: build_name_generator(
            (YetiNameGenerator1, 0, 6),
            (YetiNameGenerator2, 6, 8),
            (YetiNameGenerator3, 8, 10),
        ),
    })
