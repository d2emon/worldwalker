from ..database import db_data_provider
from genelib import SyllablicGenerator, GenderedNameGenerator, ComplexNameGenerator, Gendered, build_name_generator
from genelib.genders import GENDER_NEUTRAL, GENDER_MALE, GENDER_FEMALE


class BaseWizardNameGenerator(SyllablicGenerator):
    NAME_V1 = 1
    NAME_V2 = 2
    NAME_V3 = 3

    default_providers = {
        'nm1': db_data_provider('wizard', 'nm1'),
        'nm2': db_data_provider('wizard', 'nm2'),
        'nm3': db_data_provider('wizard', 'nm3'),
        'nm4': db_data_provider('wizard', 'nm4'),
        'nm5': db_data_provider('wizard', 'nm5'),
        'nm6': db_data_provider('wizard', 'nm6'),
        'nm7': db_data_provider('wizard', 'nm7'),
        'nm8': db_data_provider('wizard', 'nm8'),
        'nm9': db_data_provider('wizard', 'nm9'),
        'nm10': db_data_provider('wizard', 'nm10'),
        'nm11': db_data_provider('wizard', 'nm11'),
    }
    name_type = NAME_V1

    @classmethod
    def join_syllables(cls, syllables, inner1=(), inner2=(), *args):
        return cls.GLUE.join([str(syllable) for syllable in syllables])


class BaseFemaleWizardNameGenerator(BaseWizardNameGenerator):
    pass


class BaseMaleWizardNameGenerator(BaseWizardNameGenerator):
    pass


class BaseNeutralWizardNameGenerator(BaseWizardNameGenerator):
    pass


class FemaleWizardNameGenerator1(BaseFemaleWizardNameGenerator):
    syllable_providers = {
        3: db_data_provider('wizard', 'nm3'),
        6: db_data_provider('wizard', 'nm8'),
    }

    def name(self):
        syllables = self.syllables()
        return self.join_syllables([
            syllables[3],
            syllables[6],
        ])


class FemaleWizardNameGenerator2(BaseFemaleWizardNameGenerator):
    name_type = BaseWizardNameGenerator.NAME_V2

    syllable_providers = {
        2: db_data_provider('wizard', 'nm6'),
        5: db_data_provider('wizard', 'nm3'),
        6: db_data_provider('wizard', 'nm8'),
    }

    def rules(self, syllables):
        while str(syllables[2]) == str(syllables[6]):
            syllables[2] = next(self.syllable_generators[2])
        return syllables

    def name(self):
        syllables = self.syllables()
        return self.join_syllables([
            syllables[2],
            syllables[5],
            syllables[6],
        ])


class FemaleWizardNameGenerator3(BaseFemaleWizardNameGenerator):
    name_type = BaseWizardNameGenerator.NAME_V3

    syllable_providers = {
        1: db_data_provider('wizard', 'nm1'),
        2: db_data_provider('wizard', 'nm7'),
        5: db_data_provider('wizard', 'nm3'),
        6: db_data_provider('wizard', 'nm8'),
    }

    def rules(self, syllables):
        while str(syllables[2]) == str(syllables[6]):
            syllables[2] = next(self.syllable_generators[2])
        return syllables

    def name(self):
        syllables = self.syllables()
        return self.join_syllables([
            syllables[1],
            syllables[2],
            syllables[5],
            syllables[6],
        ])


class MaleWizardNameGenerator1(BaseMaleWizardNameGenerator):
    syllable_providers = {
        5: db_data_provider('wizard', 'nm3'),
        6: db_data_provider('wizard', 'nm5'),
    }

    def name(self):
        syllables = self.syllables()
        return self.join_syllables([
            syllables[5],
            syllables[6],
        ])


class MaleWizardNameGenerator2(BaseMaleWizardNameGenerator):
    name_type = BaseWizardNameGenerator.NAME_V2

    syllable_providers = {
        2: db_data_provider('wizard', 'nm2'),
        5: db_data_provider('wizard', 'nm3'),
        6: db_data_provider('wizard', 'nm5'),
    }

    def rules(self, syllables):
        while str(syllables[2]) == str(syllables[6]):
            syllables[2] = next(self.syllable_generators[2])
        return syllables

    def name(self):
        syllables = self.syllables()
        return self.join_syllables([
            syllables[2],
            syllables[5],
            syllables[6],
        ])


class MaleWizardNameGenerator3(BaseMaleWizardNameGenerator):
    name_type = BaseWizardNameGenerator.NAME_V3

    syllable_providers = {
        1: db_data_provider('wizard', 'nm1'),
        2: db_data_provider('wizard', 'nm4'),
        5: db_data_provider('wizard', 'nm3'),
        6: db_data_provider('wizard', 'nm5'),
    }

    def rules(self, syllables):
        while str(syllables[2]) == str(syllables[6]):
            syllables[2] = next(self.syllable_generators[2])
        return syllables

    def name(self):
        syllables = self.syllables()
        return self.join_syllables([
            syllables[1],
            syllables[2],
            syllables[5],
            syllables[6],
        ])


class WizardNameGenerator1(BaseNeutralWizardNameGenerator):
    syllable_providers = {
        5: db_data_provider('wizard', 'nm3'),
        6: db_data_provider('wizard', 'nm9'),
    }

    def name(self):
        syllables = self.syllables()
        return self.join_syllables([
            syllables[5],
            syllables[6],
        ])


class WizardNameGenerator2(BaseNeutralWizardNameGenerator):
    name_type = BaseWizardNameGenerator.NAME_V2

    syllable_providers = {
        2: db_data_provider('wizard', 'nm10'),
        5: db_data_provider('wizard', 'nm3'),
        6: db_data_provider('wizard', 'nm9'),
    }

    def rules(self, syllables):
        while str(syllables[2]) == str(syllables[6]):
            syllables[2] = next(self.syllable_generators[2])
        return syllables

    def name(self):
        syllables = self.syllables()
        return self.join_syllables([
            syllables[2],
            syllables[5],
            syllables[6],
        ])


class WizardNameGenerator3(BaseNeutralWizardNameGenerator):
    name_type = BaseWizardNameGenerator.NAME_V3

    syllable_providers = {
        1: db_data_provider('wizard', 'nm1'),
        2: db_data_provider('wizard', 'nm11'),
        5: db_data_provider('wizard', 'nm3'),
        6: db_data_provider('wizard', 'nm9'),
    }

    def rules(self, syllables):
        while str(syllables[2]) == str(syllables[6]):
            syllables[2] = next(self.syllable_generators[2])
        return syllables

    def name(self):
        syllables = self.syllables()
        return self.join_syllables([
            syllables[1],
            syllables[2],
            syllables[5],
            syllables[6],
        ])


class Wizard(Gendered):
    """
    Wizard names vary greatly from one work of fiction to another. Some choose to stick more to real names, like many
    names in Harry Potter, while others stick to fantasy-style names, like in Lord of the Rings.

    This generator generally sticks to the fantasy-style names, as there are plenty of name generators for real names.
    However, there are plenty of names which could also be used as a fairly unique real name.

    I've also tried to make sure many different types of fantasy styles are part of this generator, from the more
    easily pronounceable friendly names, to the less pronounceable, demonic or evil sounding names.
    """
    MALE = GENDER_MALE
    FEMALE = GENDER_FEMALE
    NEUTRAL = GENDER_NEUTRAL

    name_generator = GenderedNameGenerator({
        MALE: ComplexNameGenerator([
            MaleWizardNameGenerator1,
            MaleWizardNameGenerator2,
            MaleWizardNameGenerator3,
        ]),
        FEMALE: ComplexNameGenerator([
            FemaleWizardNameGenerator1,
            FemaleWizardNameGenerator2,
            FemaleWizardNameGenerator3,
        ]),
        NEUTRAL: ComplexNameGenerator([
            WizardNameGenerator1,
            WizardNameGenerator2,
            WizardNameGenerator3,
        ]),
    })
