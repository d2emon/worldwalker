from genelib.descriptionGenerator import DescriptionGenerator
from ..database import get_providers_from_db
from .descriptive import Descriptive
from ..database.descr.realm import DATA

import random


MOVEMENTS__ = 'nm1-ru'
PORTAL_TYPES__ = 'nm2-ru'
PORTAL_DESCRIPTIONS__ = 'nm3-ru'
WORLD_TYPES__ = 'nm4-ru'
WORLD_DESCRIPTIONS__ = 'nm6-ru'
WORLD_DESCRIPTIONS_GOOD__ = 'nm5-ru-good'
WORLD_DESCRIPTIONS_BAD__ = 'nm5-ru-bad'


class Movement:
    movements = DATA[MOVEMENTS__]

    def __init__(self):
        self.movement = random.choice(self.movements)

    def __str__(self):
        return "Вы {}".format(self.movement)


class Portal:
    portal_types = DATA[PORTAL_TYPES__]
    descriptions = DATA[PORTAL_DESCRIPTIONS__]

    def __init__(self):
        self.portal_type = random.choice(self.portal_types)
        self.short_description = random.choice(self.descriptions)

    def __str__(self):
        return "{} портал".format(self.portal_type)

    @property
    def description(self):
        return "{}, {}".format(self, self.short_description)


class World:
    world_types = DATA[WORLD_TYPES__]
    descriptions = DATA[WORLD_DESCRIPTIONS__]
    descriptions_good = DATA[WORLD_DESCRIPTIONS_GOOD__]
    descriptions_bad = DATA[WORLD_DESCRIPTIONS_BAD__]
    nm7 = DATA['nm7']
    nm8 = DATA['nm9']
    nm9 = DATA['nm9']
    nm10 = DATA['nm10']

    def __init__(self):
        self.world_type = random.choice(self.world_types)

        if self.is_bad:
            self.__description_parts1 = [random.choice(self.descriptions_bad) + "."]
        else:
            self.__description_parts1 = [random.choice(self.descriptions_good) + "."]
        self.__description_parts1.append(random.choice(self.descriptions) + ".")

        data7 = random.choice(self.nm7)
        data8 = random.choice(self.nm8)
        if self.nm7.index(data7) < 5:
            while self.nm8.index(data8) > 4:
                data8 = random.choice(self.nm8)
        elif self.nm7.index(data7) < 10:
            while self.nm8.index(data8) < 5 or self.nm8.index(data8) > 9:
                data8 = random.choice(self.nm8)
        elif self.nm7.index(data7) < 15:
            while self.nm8.index(data8) < 10 or self.nm8.index(data8) > 14:
                data8 = random.choice(self.nm8)
        else:
            while self.nm8.index(data8) < 15:
                data8 = random.choice(self.nm8)

        self.__description_parts2 = [data7 + data8 + "."]
        self.__description_parts2.append("Этот мир - {}{}.".format(
            random.choice(self.nm9),
            random.choice(self.nm10),
        ))

    @property
    def is_bad(self):
        return self.world_types.index(self.world_type) < 15

    @property
    def description(self):
        return "\n".join([
            " ".join(self.__description_parts1),
            " ".join(self.__description_parts2),
        ])

    def __str__(self):
        return "{} мир".format(self.world_type)


class RealmOld:
    nm11 = DATA['nm11']
    nm12 = DATA['nm12']
    nm13 = DATA['nm13']
    nm14 = DATA['nm14']
    nm15 = DATA['nm15']
    nm16 = DATA['nm16']
    nm17 = DATA['nm17']
    nm18 = DATA['nm18']
    nm19 = DATA['nm19']
    nm20 = DATA['nm20']
    nm21 = DATA['nm21']

    def __init__(self):
        self.portal = Portal()
        self.world = World()

        self.data = {
            11: random.choice(self.nm11),
            12: random.choice(self.nm12),
            13: random.choice(self.nm13),
            14: random.choice(self.nm14),
            15: random.choice(self.nm15),
            16: random.choice(self.nm16),
            17: random.choice(self.nm17),
            '17b': random.choice(self.nm17),
            '17c': random.choice(self.nm17),

            18: random.choice(self.nm18),
            19: random.choice(self.nm19),
            20: random.choice(self.nm20),
            '20b': random.choice(self.nm20),
            '20c': random.choice(self.nm20),

            21: random.choice(self.nm21),
        }

        while self.data['17b'] == self.data[17]:
            self.data['17b'] = random.choice(self.nm17)
        while self.data['17c'] in (self.data[17], self.data['17b']):
            self.data['17c'] = random.choice(self.nm17)

        while self.data['20b'] == self.data[20]:
            self.data['20b'] = random.choice(self.nm20)
        while self.data['20c'] in (self.data[20], self.data['20b']):
            self.data['20c'] = random.choice(self.nm20)

    def show(self):
        movement = Movement()

        text = [
            "{} сквозь {}. Вас сразу же встречает {}. {} ".format(
                movement,
                self.portal.description,
                self.world,
                self.world.description,
            ),
            "{} you {} of {}. {}, {}. {} {} creatures, {} creatures, and what you think might be {} creatures of some sort.".format(
                self.data[11],
                self.data[12],
                self.data[13],
                self.data[14],
                self.data[15],
                self.data[16],
                self.data[17],
                self.data['17b'],
                self.data['17c'],

            ),
            "{} as {}. But, with {}, {}, and {}, {}.".format(
                self.data[18],
                self.data[19],
                self.data[20],
                self.data['20b'],
                self.data['20c'],
                self.data[21],
            ),
        ]

        return ''.join([
            text[0],
            "\n",
            "\n",
            text[1],
            "\n",
            "\n",
            text[2],
        ])


MOVEMENT = 'nm1'
PORTAL_TYPE = 'nm2'
PORTAL_DESCRIPTION = 'nm3'
WORLD_TYPE = 'nm4'
WORLD_DESCRIPTION_1 = 'nm5'
WORLD_DESCRIPTION_2 = 'nm6'

WORLD_FIRST_SIGHT = 'nm7'
WORLD_SECOND_SIGHT = 'nm8'
WORLD_SHORT = 'nm9'
WORLD_SUMMARY = 'nm10'

DISTANCE = 'nm11'
FEELING = 'nm12'
CREATURE_DESCRIPTION = 'nm13'
CREATURE_FIRST_SIGHT = 'nm14'
CREATURE_SUMMARY = 'nm15'
DECISION = 'nm16'
CREATURE_TYPE = 'nm17'

ADVENTURE_REQUIREMENTS = 'nm18'
ADVENTURE_BEGIN = 'nm19'
ADVENTURE_QUALITIES = 'nm20'
ADVENTURE_CONTINUE = 'nm21'


PROVIDERS = {
    **get_providers_from_db('realm'),
}
DATA_GENERATORS = {
    'rnd1': MOVEMENT,
    'rnd2': PORTAL_TYPE,
    'rnd3': PORTAL_DESCRIPTION,
    'rnd4': WORLD_TYPE,
    'rnd5': WORLD_DESCRIPTION_1,
    'rnd6': WORLD_DESCRIPTION_2,

    'rnd7': WORLD_FIRST_SIGHT,
    'rnd8': WORLD_SECOND_SIGHT,
    'rnd9': WORLD_SHORT,
    'rnd10': WORLD_SUMMARY,

    'rnd11': DISTANCE,
    'rnd12': FEELING,
    'rnd13': CREATURE_DESCRIPTION,
    'rnd14': CREATURE_FIRST_SIGHT,
    'rnd15': CREATURE_SUMMARY,
    'rnd16': DECISION,
    'rnd17': CREATURE_TYPE,
    'rnd17b': CREATURE_TYPE,
    'rnd17c': CREATURE_TYPE,

    'rnd18': ADVENTURE_REQUIREMENTS,
    'rnd19': ADVENTURE_BEGIN,
    'rnd20': ADVENTURE_QUALITIES,
    'rnd20b': ADVENTURE_QUALITIES,
    'rnd20c': ADVENTURE_QUALITIES,
    'rnd21': ADVENTURE_CONTINUE,
}
TEMPLATES = {
    'name1': "You {rnd1} forward through the {rnd2} portal {rnd3}. You're immediately met by {rnd4} world. {rnd5}. "
             "{rnd6}. ",
    'name2': "{rnd7}{rnd8}. This world is {rnd9}{rnd10}.",

    'name3': "{rnd11} you {rnd12} of {rnd13}. {rnd14}, {rnd15}. {rnd16} {rnd17} creatures, {rnd17b} creatures, and "
             "what you think might be {rnd17c} creatures of some sort.",

    'name4': "{rnd18} as {rnd19}. But, with {rnd20}, {rnd20b}, and {rnd20c}, {rnd21}.",
}
TEXT = "\n".join([
    "{name1}\n{name2}\n",
    "{name3}\n",
    "{name4}"
])


def valid_rnd5(item, data):
    if data['rnd4'].item_id >= 15:
        return True
    return item.item_id <= 19


def valid_rnd8(item, data):
    if data['rnd7'].item_id < 5:
        return item.item_id > 4
    if 4 < data['rnd7'].item_id < 10:
        return item.item_id < 5 or item.item_id > 9
    if 9 < data['rnd7'] .item_id < 15:
        return item.item_id < 10 or item.item_id > 14
    if 14 < data['rnd7'].item_id:
        return item.item_id < 15
    return True


class RealmDescriptionGenerator(DescriptionGenerator):
    def __init__(self, providers):
        super().__init__(providers)
        self.generators = DATA_GENERATORS
        self.rules = {
            'rnd5': valid_rnd5,
            'rnd8': valid_rnd8,
            'rnd17b': self.unique('rnd17'),
            'rnd17c': self.unique('rnd17', 'rnd11b'),
            'rnd20b': self.unique('rnd20'),
            'rnd20c': self.unique('rnd20', 'rnd20b'),
        }
        self.templates = TEMPLATES
        self.text = TEXT


class Realm(Descriptive):
    """
    Some aspects of the descriptions will remain the same, this is done to keep the general structure the same, while
    still randomizing the important details. This way it's easier for you to add your own details, like making it a
    futuristic version or a steampunk version.

    The descriptions mainly stick to a fairly realistic version of a shotgun, but even this generator doesn't cover
    every single type of shotgun available today. The fantasy or other extra details are easy to add on your own and
    they weren't added on purpose to make sure your weapons are more original and are more authentic to the world you've
    created.
    """
    description_generator = RealmDescriptionGenerator(PROVIDERS)
