from genelib.descriptionGenerator import DescriptionGenerator
from ...database import get_providers, LengthProvider
from .weapon import Weapon


STAFF_PROVIDERS = {
    **get_providers('staff'),
    'nm1': LengthProvider(160, 220),
}
STAFF_GENERATORS = {
    'nm1': 'nm1',
    'rnd2': 'nm2',
    'rnd3': 'nm3',
    'rnd4': 'nm4',
    'rnd5': 'nm5',
    'rnd6': 'nm6',
    'rnd7': 'nm7',
    'rnd8': 'nm8',
    'rnd9': 'nm9',
    'rnd10': 'nm10',
    'rnd11': 'nm2',
    'rnd12': 'nm8',
    'rnd13': 'nm9',
}
STAFF_TEMPLATES = {
    'name1': "{nm1.cm} centimeters ({nm1.inches} inches) of {rnd2} {rnd3} form the base of this {rnd4} staff. {rnd5}, "
             "which has been {rnd6}.",
    'name2': "The bottom ends in {rnd7} made of {rnd8} and has been decorated with {rnd9}.",
    'name3': "The top is made out of {rnd11} {rnd12} and has been crafted into {rnd10}, which has been decorated with "
             "{rnd13}.",
}
STAFF_TEXT = "{name1}\n\n{name2}\n\n{name3}"


class StaffDescriptionGenerator(DescriptionGenerator):
    def __init__(self, providers):
        super().__init__(providers)
        self.generators = STAFF_GENERATORS
        self.rules = {
            'nm13': self.unique('nm13', 'nm9'),
        }
        self.templates = STAFF_TEMPLATES
        self.text = STAFF_TEXT


class Staff(Weapon):
    description_generator = StaffDescriptionGenerator(STAFF_PROVIDERS)
