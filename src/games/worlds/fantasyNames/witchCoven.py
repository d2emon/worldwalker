from genelib.fng.named import Named
from genelib.fng.namegen import NameFactory
from ..database.provider import group_providers_from_list
from games.worlds.genelib import build_name_generator


DATABASE = 'witch-coven'
PARTS = [
    'nm1',  # nm1.splice(rnd, 1)
    'nm2',  # nm2.splice(rnd, 1)
    'nm3',
]


class BaseWitchCovenNameGenerator(NameFactory):
    NAME_V1 = 1
    NAME_V2 = 2
    name_type = NAME_V1
    default_providers = group_providers_from_list(DATABASE, PARTS)
    used_parts = PARTS


class WitchCovenNameGenerator1(BaseWitchCovenNameGenerator):
    name_type = BaseWitchCovenNameGenerator.NAME_V1
    template = "The {nm1} {nm3}"


class WitchCovenNameGenerator2(BaseWitchCovenNameGenerator):
    name_type = BaseWitchCovenNameGenerator.NAME_V2
    template = "{nm3} of {nm2}"


class WitchCoven(Named):
    """
    A coven is a group of witches, which can come in different forms depending on the type of witchcraft the witches
    belong to. The coven might be a community of many, a mere handful or anything in between. It could be a permanent
    group or merely a temporary gathering and so on.

    Coven names can also vary greatly, although I did notice several themes in existing coven names and I used these
    themes for the names in this generator. A coven's name is usually a very personal choice however, but hopefully
    this name generator will be helpful nonetheless.
    """

    class NameFactory(Named.NameFactory):
        factory = build_name_generator(
            (WitchCovenNameGenerator1, 0, 5),
            (WitchCovenNameGenerator2, 5, 10),
        )
