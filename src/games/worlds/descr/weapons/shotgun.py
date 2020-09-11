from ...genelib.descriptionGenerator import DescriptionGenerator
from ...database.provider import list_providers
from ...database.provider.number_data import NumberDataProvider
from .weapon import Weapon


PROVIDERS = {
    **list_providers('shotgun'),
    'nm6': NumberDataProvider(600, 1100),
    'nm7_2': NumberDataProvider(100, 300),
    'nm8': NumberDataProvider(21, 48, 10),
}
DATA_GENERATORS = {
    'rnd1': 'nm1',
    'rnd2': 'nm2',
    'rnd3': 'nm3',
    'rnd4': 'nm4',
    'rnd5': 'nm5',
    'nm6': 'nm6',
    'nm7_2': 'nm7_2',
    'nm8': 'nm8',
    'rnd9': 'nm9',
    'rnd10': 'nm10',
    'rnd11a': 'nm11',
    'rnd11b': 'nm11',
    'rnd11c': 'nm11',
    'rnd11d': 'nm11',
    'rnd12a': 'nm12',
    'rnd12b': 'nm12',
    'rnd12c': 'nm12',
    'rnd13a': 'nm13',
    'rnd13b': 'nm13',
    'rnd13c': 'nm13',
    'rnd14a': 'nm14',
    'rnd14b': 'nm14',
    'rnd14c': 'nm14',
    'rnd15': 'nm15',
    'rnd16': 'nm16',
    'rnd16a': 'nm16',
    'rnd16b': 'nm16',
    'rnd16c': 'nm16',
    'rnd17a': 'nm17',
    'rnd17b': 'nm17',
    'rnd18a': 'nm18',
    'rnd18b': 'nm18',
    'rnd18c': 'nm18',
    'rnd18d': 'nm18',
    'rnd19': 'nm19',
}
TEMPLATES = {
    'name1': "This {rnd1} shotgun is {rnd2}, it's used {rnd3} as it's {rnd4}.",
    'name2': "The {rnd5} of the weapon is {nm6}mm and has a barrel length of {nm7}mm. The weapon weighs {nm8}kg.",
    'name3': "The caliber used in this weapon is a {rnd9} and uses a {rnd10} firing mechanism. The ammo used most "
             "commonly are {rnd11a}, but it also takes {rnd11b}, {rnd11c} and {rnd11d}.",

    'name4': "This shotgun comes with {rnd12a}, but {rnd12b} and {rnd12c} are also available.",
    'name5': "The stock is made out of {rnd13a}, but it can also be made out of {rnd13b} and {rnd13c} if you so "
             "desire.",
    'name6': "There are {rnd14a} on the stock, but {rnd14b} or {rnd14c} are available as well.",

    'name7': "This weapon was designed by a {rnd15} who initially disgned it for use in {rnd16}, today it's used for "
             "{rnd16a}, {rnd16b} and {rnd16c}.",
    'name8': "The name of this weapon is the {rnd17a}{rnd17b}-{rnd18a}{rnd18b}{rnd18c}{rnd18d}, but it usually goes by "
             "its nickname, {rnd19}.",
}
TEXT = "\n".join([
    "{name1}\n{name2}\n{name3}\n",
    "{name4}\n{name5}\n{name6}\n",
    "{name7}\n{name8}"
])


class ShotgunDescriptionGenerator(DescriptionGenerator):
    def __init__(self, providers):
        super().__init__(providers)
        self.generators = DATA_GENERATORS
        self.rules = {
            'rnd11b': self.unique('rnd11a'),
            'rnd11c': self.unique('rnd11a', 'rnd11b'),
            'rnd11d': self.unique('rnd11a', 'rnd11b', 'rnd11c'),
            'rnd12b': self.unique('rnd12a'),
            'rnd12c': self.unique('rnd12a', 'rnd12b'),
            'rnd13b': self.unique('rnd13a'),
            'rnd13c': self.unique('rnd13a', 'rnd13b'),
            'rnd14b': self.unique('rnd14a'),
            'rnd14c': self.unique('rnd14a', 'rnd14b'),
            'rnd16b': self.unique('rnd16a'),
            'rnd16c': self.unique('rnd16a', 'rnd16b'),
        }
        self.templates = TEMPLATES
        self.text = TEXT

    @classmethod
    def barrel_length(cls, data):
        return

    def generate_from_data(self, **data):
        items = super().generate_from_data(**data)
        return {
            **items,
            'nm7': items['nm6'] - items['nm7_2'],
        }


class Shotgun(Weapon):
    """
    Some aspects of the descriptions will remain the same, this is done to keep the general structure the same, while
    still randomizing the important details. This way it's easier for you to add your own details, like making it a
    futuristic version or a steampunk version.

    The descriptions mainly stick to a fairly realistic version of a shotgun, but even this generator doesn't cover
    every single type of shotgun available today. The fantasy or other extra details are easy to add on your own and
    they weren't added on purpose to make sure your weapons are more original and are more authentic to the world you've
    created.
    """
    description_generator = ShotgunDescriptionGenerator(PROVIDERS)
