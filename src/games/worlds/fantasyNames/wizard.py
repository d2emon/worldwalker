from ..database import get_data_providers, get_syllable_providers
from ..genelib import SyllablicGenerator, GenderedNameGenerator, ComplexNameGenerator, Gendered
from ..genelib.genders import GENDER_NEUTRAL, GENDER_MALE, GENDER_FEMALE


class BaseWizardNameGenerator(SyllablicGenerator):
    NAME_V1 = 1
    NAME_V2 = 2
    NAME_V3 = 3
    name_type = NAME_V1
    default_providers = get_data_providers('wizard', [
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
    ])
    templates = {
        NAME_V1: (5, 6),
        NAME_V2: (2, 5, 6),
        NAME_V3: (1, 2, 5, 6),
    }

    @classmethod
    def template(cls):
        return cls.templates[cls.name_type]


class WizardNameRulesV1(BaseWizardNameGenerator):
    name_type = BaseWizardNameGenerator.NAME_V1

    def name_rules(self):
        return dict()


class WizardNameRulesV2(WizardNameRulesV1):
    name_type = BaseWizardNameGenerator.NAME_V2

    def name_rules(self):
        def unique_with_6(syllable, syllables):
            return str(syllable) != str(syllables[6])[0]
        return {2: unique_with_6}


class WizardNameRulesV3(WizardNameRulesV2):
    name_type = BaseWizardNameGenerator.NAME_V3


class BaseMaleWizardNameGenerator(BaseWizardNameGenerator):
    gender = GENDER_MALE


class BaseNeutralWizardNameGenerator(BaseWizardNameGenerator):
    gender = GENDER_NEUTRAL


class BaseFemaleWizardNameGenerator(BaseWizardNameGenerator):
    gender = GENDER_FEMALE


class MaleWizardNameGenerator1(WizardNameRulesV1, BaseMaleWizardNameGenerator):
    syllable_providers = get_syllable_providers('wizard', {
        5: 'nm3',
        6: 'nm5',
    })


class MaleWizardNameGenerator2(WizardNameRulesV2, BaseMaleWizardNameGenerator):
    syllable_providers = get_syllable_providers('wizard', {
        2: 'nm2',
        5: 'nm3',
        6: 'nm5',
    })


class MaleWizardNameGenerator3(WizardNameRulesV3, BaseMaleWizardNameGenerator):
    syllable_providers = get_syllable_providers('wizard', {
        1: 'nm1',
        2: 'nm4',
        5: 'nm3',
        6: 'nm5',
    })


class FemaleWizardNameGenerator1(WizardNameRulesV1, BaseFemaleWizardNameGenerator):
    syllable_providers = get_syllable_providers('wizard', {
        5: 'nm3',
        6: 'nm8',
    })


class FemaleWizardNameGenerator2(WizardNameRulesV2, BaseFemaleWizardNameGenerator):
    syllable_providers = get_syllable_providers('wizard', {
        2: 'nm6',
        5: 'nm3',
        6: 'nm8',
    })


class FemaleWizardNameGenerator3(WizardNameRulesV3, BaseFemaleWizardNameGenerator):
    syllable_providers = get_syllable_providers('wizard', {
        1: 'nm1',
        2: 'nm7',
        5: 'nm3',
        6: 'nm8',
    })


class WizardNameGenerator1(WizardNameRulesV1, BaseNeutralWizardNameGenerator):
    syllable_providers = get_syllable_providers('wizard', {
        5: 'nm3',
        6: 'nm9',
    })


class WizardNameGenerator2(WizardNameRulesV2, BaseNeutralWizardNameGenerator):
    syllable_providers = get_syllable_providers('wizard', {
        2: 'nm10',
        5: 'nm3',
        6: 'nm9',
    })


class WizardNameGenerator3(WizardNameRulesV3, BaseNeutralWizardNameGenerator):
    syllable_providers = get_syllable_providers('wizard', {
        1: 'nm1',
        2: 'nm11',
        5: 'nm3',
        6: 'nm9',
    })


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
