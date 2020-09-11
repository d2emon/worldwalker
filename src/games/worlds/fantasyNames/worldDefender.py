from genelib.fng.named import Named
from genelib.fng.namegen import NameFactory
from ..database.provider import group_providers_from_list
from games.worlds.genelib import build_name_generator


DATABASE = 'world-defender'
PARTS = [
    'nm1',
    'nm2',  # nm2.splice(rnd2, 1)
    'nm3',  # nm3.splice(rnd, 1)
    'nm4',
]


class BaseWorldDefenderNameGenerator(NameFactory):
    NAME_V1 = 1
    NAME_V2 = 2
    NAME_V3 = 3
    NAME_V4 = 4
    name_type = NAME_V1
    default_providers = group_providers_from_list(DATABASE, PARTS)
    used_parts = PARTS


class WorldDefenderNameGenerator1(BaseWorldDefenderNameGenerator):
    name_type = BaseWorldDefenderNameGenerator.NAME_V1
    template = "The {nm1} {nm3}"


class WorldDefenderNameGenerator2(BaseWorldDefenderNameGenerator):
    name_type = BaseWorldDefenderNameGenerator.NAME_V2
    template = "{nm2} of {nm4}"


class WorldDefenderNameGenerator3(BaseWorldDefenderNameGenerator):
    name_type = BaseWorldDefenderNameGenerator.NAME_V3
    template = "The {nm3} of {nm2}"


class WorldDefenderNameGenerator4(BaseWorldDefenderNameGenerator):
    name_type = BaseWorldDefenderNameGenerator.NAME_V4
    template = "The {nm3} {nm1} {nm2}"


class WorldDefender(Named):
    """
    There are all sorts of world defenders of course. Godly beings with vast powers, fighters who've sworn to protect
    all life, or even just a humble activist trying to make the world a better place. While this generator generally
    focuses more on the fantasy themed world defenders, the names in this generator could fit every kind of world
    defender.

    The names in this generator, which could arguably simply be called titles, come in the forms of names like 'The
    World Warden', 'Keeper of Life', and 'The Ancient Shepherd'. Some names will fit certain types of defenders better
    than others, but there's plenty to pick from, so you're bound to find a name that suits your needs.
    """
    name_generator = build_name_generator(
        (WorldDefenderNameGenerator1, 0, 3),
        (WorldDefenderNameGenerator2, 3, 6),
        (WorldDefenderNameGenerator3, 6, 8),
        (WorldDefenderNameGenerator4, 8, 10),
    )
