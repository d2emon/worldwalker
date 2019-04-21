from ..database import get_data_providers
from genelib import NameGenerator, Named, build_name_generator


DATABASE = 'world-destroyer'
PARTS = [
    'nm1',
    'nm2',  # nm2.splice(rnd2, 1)
    'nm3',  # nm3.splice(rnd, 1)
    'nm4',
]


class BaseWorldDestroyerNameGenerator(NameGenerator):
    NAME_V1 = 1
    NAME_V2 = 2
    NAME_V3 = 3
    NAME_V4 = 4
    name_type = NAME_V1
    default_providers = get_data_providers(DATABASE, PARTS)
    used_parts = PARTS


class WorldDestroyerNameGenerator1(BaseWorldDestroyerNameGenerator):
    name_type = BaseWorldDestroyerNameGenerator.NAME_V1
    template = "The {nm1} {nm2}"


class WorldDestroyerNameGenerator2(BaseWorldDestroyerNameGenerator):
    name_type = BaseWorldDestroyerNameGenerator.NAME_V2
    template = "{nm2} of {nm4}"


class WorldDestroyerNameGenerator3(BaseWorldDestroyerNameGenerator):
    name_type = BaseWorldDestroyerNameGenerator.NAME_V3
    template = "The {nm3} of {nm2}"


class WorldDestroyerNameGenerator4(BaseWorldDestroyerNameGenerator):
    name_type = BaseWorldDestroyerNameGenerator.NAME_V4
    template = "The {nm3} {nm1} {nm2}"


class WorldDestroyer(Named):
    """
    World destroyers come in many different shapes and sizes, from a relatively small creature with (un)godly powers to
    massive, planet-sized beings who consume entire galaxies. This name generator is aimed at all of those and anything
    in between, though, to some extent, you could see the names in this generator as titles, rather than as names.
    You'll find results like 'Ruiner of Realms', 'The Grand Consumer' and 'Undoer of Life'.

    If you combine them you could end up with a long sequence of titles, similar to how royalty sometimes has multiple
    titles, but in a more gruesome way when it comes to world destroyers.
    """
    name_generator = build_name_generator(
        (WorldDestroyerNameGenerator1, 0, 3),
        (WorldDestroyerNameGenerator2, 3, 6),
        (WorldDestroyerNameGenerator3, 6, 8),
        (WorldDestroyerNameGenerator4, 8, 10),
    )
