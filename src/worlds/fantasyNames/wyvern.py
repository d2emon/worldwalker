from ..database import db_data_provider
from genelib import SyllablicGenerator, Gendered


class BaseWyvernNameGenerator(SyllablicGenerator):
    """
    Wyverns are creatures similar to dragons, except they only have 2 legs and usually a barbed tail. Wyverns usually
    also don't breathe fire either, but their bite is venemous. However, all these details vary from work of fiction to
    work of fiction.

    As far as names go, wyvern names tend to be far more vicious sounding than their dragon counterparts, perhaps
    because wyverns are often depicted as less intelligent and more animalistic and aggressive or perhaps for a
    different reason entirely. Either way I focused on these kinds of names in this generator. If you are looking for
    more melodic names the dragon name generator is a great place to start.
    """
    NAME_V1 = 1
    NAME_V2 = 2

    default_providers = {
        'nm1': db_data_provider('wyvern', 'nm1'),
        'nm2': db_data_provider('wyvern', 'nm2'),
        'nm3': db_data_provider('wyvern', 'nm3'),
        'nm4': db_data_provider('wyvern', 'nm4'),
        'nm5': db_data_provider('wyvern', 'nm5'),
        'nm6': db_data_provider('wyvern', 'nm6'),
        'nm7': db_data_provider('wyvern', 'nm7'),
        'nm8': db_data_provider('wyvern', 'nm8'),
        'nm9': db_data_provider('wyvern', 'nm9'),
        'nm10': db_data_provider('wyvern', 'nm10'),
        'nm11': db_data_provider('wyvern', 'nm11'),
        'nm12': db_data_provider('wyvern', 'nm12'),
        'nm13': db_data_provider('wyvern', 'nm13'),
        'nm14': db_data_provider('wyvern', 'nm14'),
        'nm15': db_data_provider('wyvern', 'nm15'),
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
        syllables = self.unique_syllables(syllables, 5, 3)
        return syllables

    def name(self):
        syllables = self.syllables()
        if self.name_type == self.NAME_V2:
            return self.join_syllables(
                syllables,
                [],
                [syllables[6], syllables[7]]
            )
        return self.join_syllables(syllables)


class BaseFemaleWyvernNameGenerator(BaseWyvernNameGenerator):
    syllable_providers = {
        1: db_data_provider('wyvern', 'nm6'),
        2: db_data_provider('wyvern', 'nm7'),
        3: db_data_provider('wyvern', 'nm8'),
        4: db_data_provider('wyvern', 'nm7'),
        5: db_data_provider('wyvern', 'nm10'),

        6: db_data_provider('wyvern', 'nm9'),
        7: db_data_provider('wyvern', 'nm7'),
    }


class BaseMaleWyvernNameGenerator(BaseWyvernNameGenerator):
    syllable_providers = {
        1: db_data_provider('wyvern', 'nm1'),
        2: db_data_provider('wyvern', 'nm2'),
        3: db_data_provider('wyvern', 'nm3'),
        4: db_data_provider('wyvern', 'nm2'),
        5: db_data_provider('wyvern', 'nm5'),

        6: db_data_provider('wyvern', 'nm4'),
        7: db_data_provider('wyvern', 'nm2'),
    }


class BaseNeutralWyvernNameGenerator(BaseWyvernNameGenerator):
    syllable_providers = {
        1: db_data_provider('wyvern', 'nm11'),
        2: db_data_provider('wyvern', 'nm12'),
        3: db_data_provider('wyvern', 'nm13'),
        4: db_data_provider('wyvern', 'nm12'),
        5: db_data_provider('wyvern', 'nm15'),

        6: db_data_provider('wyvern', 'nm14'),
        7: db_data_provider('wyvern', 'nm12'),
    }


class FemaleWyvernNameGenerator1(BaseFemaleWyvernNameGenerator):
    pass


class FemaleWyvernNameGenerator2(BaseFemaleWyvernNameGenerator):
    name_type = BaseWyvernNameGenerator.NAME_V2

    def rules(self, syllables):
        syllables = super().rules(syllables)
        syllables = self.unique_syllables(syllables, 6, 3)
        return syllables


class MaleWyvernNameGenerator1(BaseMaleWyvernNameGenerator):
    pass


class MaleWyvernNameGenerator2(BaseMaleWyvernNameGenerator):
    name_type = BaseWyvernNameGenerator.NAME_V2

    def rules(self, syllables):
        syllables = super().rules(syllables)
        syllables = self.unique_syllables(syllables, 6, 3)
        return syllables


class WyvernNameGenerator1(BaseNeutralWyvernNameGenerator):
    pass


class WyvernNameGenerator2(BaseNeutralWyvernNameGenerator):
    name_type = BaseWyvernNameGenerator.NAME_V2

    def rules(self, syllables):
        syllables = super().rules(syllables)
        syllables = self.unique_syllables(syllables, 6, 3)
        return syllables


class Wyvern(Gendered):
    MALE = 1
    FEMALE = 2
    NEUTRAL = 3

    name_generators = {
        MALE: [
            MaleWyvernNameGenerator1(),
            MaleWyvernNameGenerator1(),
            MaleWyvernNameGenerator1(),
            MaleWyvernNameGenerator1(),
            MaleWyvernNameGenerator1(),
            MaleWyvernNameGenerator1(),
            MaleWyvernNameGenerator1(),
            MaleWyvernNameGenerator2(),
            MaleWyvernNameGenerator2(),
            MaleWyvernNameGenerator2(),
        ],
        FEMALE: [
            FemaleWyvernNameGenerator1(),
            FemaleWyvernNameGenerator1(),
            FemaleWyvernNameGenerator1(),
            FemaleWyvernNameGenerator1(),
            FemaleWyvernNameGenerator1(),
            FemaleWyvernNameGenerator1(),
            FemaleWyvernNameGenerator1(),
            FemaleWyvernNameGenerator2(),
            FemaleWyvernNameGenerator2(),
            FemaleWyvernNameGenerator2(),
        ],
        NEUTRAL: [
            WyvernNameGenerator1(),
            WyvernNameGenerator1(),
            WyvernNameGenerator1(),
            WyvernNameGenerator1(),
            WyvernNameGenerator1(),
            WyvernNameGenerator1(),
            WyvernNameGenerator1(),
            WyvernNameGenerator2(),
            WyvernNameGenerator2(),
            WyvernNameGenerator2(),
        ],

    }
