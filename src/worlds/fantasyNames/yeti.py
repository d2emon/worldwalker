from ..database import db_data_provider
from genelib import SyllablicGenerator, Gendered


class BaseYetiNameGenerator(SyllablicGenerator):
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
    NAME_V1 = 1
    NAME_V2 = 2
    NAME_V3 = 3

    default_providers = {
        'nm1': db_data_provider('yeti', 'nm1'),
        'nm2': db_data_provider('yeti', 'nm2'),
        'nm3': db_data_provider('yeti', 'nm3'),
        'nm4': db_data_provider('yeti', 'nm4'),
        'nm4b': db_data_provider('yeti', 'nm4b'),
        'nm5': db_data_provider('yeti', 'nm5'),
        'nm6': db_data_provider('yeti', 'nm6'),
        'nm7': db_data_provider('yeti', 'nm7'),
        'nm8': db_data_provider('yeti', 'nm8'),
        'nm9': db_data_provider('yeti', 'nm9'),
        'nm10': db_data_provider('yeti', 'nm10'),
        'nm11': db_data_provider('yeti', 'nm11'),
        'nm12': db_data_provider('yeti', 'nm12'),
        'nm13': db_data_provider('yeti', 'nm13'),
        'nm14': db_data_provider('yeti', 'nm14'),
    }
    name_type = NAME_V1

    def unique_syllables(self, syllables, syllable1, syllable2):
        syllables[syllable1] = self.unique(
            syllables[syllable1],
            syllables[syllable2],
            self.syllable_generators[syllable1]
        )
        return syllables

    def unique_5_3(self, syllables, min1, min5):
        if syllables[1].item_id < min1:
            while syllables[5].item_id < min5 or str(syllables[3]) == str(syllables[5]):
                syllables[5] = next(self.syllable_generators[5])
        return syllables

    @classmethod
    def join_syllables(cls, syllables, inner1=(), inner2=(), *args):
        return cls.GLUE.join([
            str(syllables[1]),
            str(syllables[2]),
            cls.GLUE.join([str(s) for s in inner1]),
            str(syllables[3]),
            str(syllables[4]),
            cls.GLUE.join([str(s) for s in inner2]),
            str(syllables[5]),
        ])

    def rules(self, syllables):
        syllables = self.unique_syllables(syllables, 3, 1)
        syllables = self.unique_syllables(syllables, 5, 6)
        syllables = self.unique_syllables(syllables, 6, 3)
        return syllables

    def name(self):
        syllables = self.syllables()
        if self.name_type == self.NAME_V2:
            return self.join_syllables(
                syllables,
                [],
                [syllables[6], syllables[7]]
            )
        elif self.name_type == self.NAME_V3:
            return self.join_syllables(
                syllables,
                [syllables[6], syllables[7]]
            )
        return self.join_syllables(syllables)


class BaseFemaleYetiNameGenerator(BaseYetiNameGenerator):
    syllable_providers = {
        1: db_data_provider('yeti', 'nm5'),
        2: db_data_provider('yeti', 'nm6'),
        3: db_data_provider('yeti', 'nm7'),
        4: db_data_provider('yeti', 'nm6'),
        5: db_data_provider('yeti', 'nm8'),

        6: db_data_provider('yeti', 'nm9'),
        7: db_data_provider('yeti', 'nm6'),
    }


class BaseMaleYetiNameGenerator(BaseYetiNameGenerator):
    syllable_providers = {
        1: db_data_provider('yeti', 'nm1'),
        2: db_data_provider('yeti', 'nm2'),
        3: db_data_provider('yeti', 'nm3'),
        4: db_data_provider('yeti', 'nm2'),
        5: db_data_provider('yeti', 'nm4'),

        6: db_data_provider('yeti', 'nm4b'),
        7: db_data_provider('yeti', 'nm2'),
    }


class BaseNeutralYetiNameGenerator(BaseYetiNameGenerator):
    syllable_providers = {
        1: db_data_provider('yeti', 'nm10'),
        2: db_data_provider('yeti', 'nm11'),
        3: db_data_provider('yeti', 'nm12'),
        4: db_data_provider('yeti', 'nm11'),
        5: db_data_provider('yeti', 'nm13'),

        6: db_data_provider('yeti', 'nm14'),
        7: db_data_provider('yeti', 'nm11'),
    }


class FemaleYetiNameGenerator1(BaseFemaleYetiNameGenerator):
    name_type = BaseYetiNameGenerator.NAME_V1

    def rules(self, syllables):
        syllables = self.unique_syllables(syllables, 3, 1)
        syllables = self.unique_5_3(syllables, 5, 15)
        return syllables


class FemaleYetiNameGenerator2(BaseFemaleYetiNameGenerator):
    name_type = BaseYetiNameGenerator.NAME_V2


class FemaleYetiNameGenerator3(BaseFemaleYetiNameGenerator):
    name_type = BaseYetiNameGenerator.NAME_V3


class MaleYetiNameGenerator1(BaseMaleYetiNameGenerator):
    name_type = BaseYetiNameGenerator.NAME_V1

    def rules(self, syllables):
        syllables = self.unique_syllables(syllables, 3, 1)
        syllables = self.unique_5_3(syllables, 5, 2)
        return syllables


class MaleYetiNameGenerator2(BaseMaleYetiNameGenerator):
    name_type = BaseYetiNameGenerator.NAME_V2


class MaleYetiNameGenerator3(BaseMaleYetiNameGenerator):
    name_type = BaseYetiNameGenerator.NAME_V3


class YetiNameGenerator1(BaseNeutralYetiNameGenerator):
    name_type = BaseYetiNameGenerator.NAME_V1

    def rules(self, syllables):
        syllables = self.unique_syllables(syllables, 3, 1)
        syllables = self.unique_5_3(syllables, 5, 15)
        return syllables


class YetiNameGenerator2(BaseNeutralYetiNameGenerator):
    name_type = BaseYetiNameGenerator.NAME_V2


class YetiNameGenerator3(BaseNeutralYetiNameGenerator):
    name_type = BaseYetiNameGenerator.NAME_V3


class Yeti(Gendered):
    MALE = 1
    FEMALE = 2
    NEUTRAL = 3

    name_generators = {
        MALE: [
            MaleYetiNameGenerator1(),
            MaleYetiNameGenerator1(),
            MaleYetiNameGenerator1(),
            MaleYetiNameGenerator1(),
            MaleYetiNameGenerator1(),
            MaleYetiNameGenerator1(),
            MaleYetiNameGenerator2(),
            MaleYetiNameGenerator2(),
            MaleYetiNameGenerator3(),
            MaleYetiNameGenerator3(),
        ],
        FEMALE: [
            FemaleYetiNameGenerator1(),
            FemaleYetiNameGenerator1(),
            FemaleYetiNameGenerator1(),
            FemaleYetiNameGenerator1(),
            FemaleYetiNameGenerator1(),
            FemaleYetiNameGenerator1(),
            FemaleYetiNameGenerator2(),
            FemaleYetiNameGenerator2(),
            FemaleYetiNameGenerator3(),
            FemaleYetiNameGenerator3(),
        ],
        NEUTRAL: [
            YetiNameGenerator1(),
            YetiNameGenerator1(),
            YetiNameGenerator1(),
            YetiNameGenerator1(),
            YetiNameGenerator1(),
            YetiNameGenerator1(),
            YetiNameGenerator2(),
            YetiNameGenerator2(),
            YetiNameGenerator3(),
            YetiNameGenerator3(),
        ],

    }
