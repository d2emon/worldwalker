from ...genelib.descriptionGenerator import DescriptionGenerator
from ...database import get_providers_from_db, LengthProvider
from .weapon import Weapon


PROVIDERS = {
    **get_providers_from_db('staff'),
    'nm1': LengthProvider(160, 220),
}
DATA_GENERATORS = {
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
TEMPLATES = {
    'name1': "{nm1.cm} centimeters ({nm1.inches} inches) of {rnd2} {rnd3} form the base of this {rnd4} staff. {rnd5}, "
             "which has been {rnd6}.",
    'name2': "The bottom ends in {rnd7} made of {rnd8} and has been decorated with {rnd9}.",
    'name3': "The top is made out of {rnd11} {rnd12} and has been crafted into {rnd10}, which has been decorated with "
             "{rnd13}.",
}
TEXT = "{name1}\n\n{name2}\n\n{name3}"


class StaffDescriptionGenerator(DescriptionGenerator):
    def __init__(self, providers):
        super().__init__(providers)
        self.generators = DATA_GENERATORS
        self.rules = {
            'rnd13': self.unique('rnd9'),
        }
        self.templates = TEMPLATES
        self.text = TEXT


class Staff(Weapon):
    """
    Staves can be simple and modest, like Gandalf's staff, or filled with runes, artifacts, doodads and watchamacallits,
    like those in many games. The staves in this generator mainly focus on the latter, since those are more fun to
    create and allow for more randomized details. But by ignoring some of the parts in the description you'll still get
    plenty of different, simplistic designs as well.

    As always, the descriptions have been kept vague on purpose. The goal is to make sure your interpretation of the
    same description is different from somebody else, so the result will be 2 different staves. This also allows you to
    more easily add your own touches and apply elements that might be unique to your own story universe.
    """
    description_generator = StaffDescriptionGenerator(PROVIDERS)
