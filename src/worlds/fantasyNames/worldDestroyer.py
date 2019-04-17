from ..database import db_data_provider
from genelib import NameGenerator, Named, build_name_generator


class BaseWorldDestroyerNameGenerator(NameGenerator):
    default_providers = {
        'nm1': db_data_provider('world-destroyer', 'nm1'),
        'nm2': db_data_provider('world-destroyer', 'nm2'),
        'nm3': db_data_provider('world-destroyer', 'nm3'),
        'nm4': db_data_provider('world-destroyer', 'nm4'),
    }


class WorldDestroyerNameGenerator1(BaseWorldDestroyerNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm1']),
            2: next(self.data['nm2']),  # nm2.splice(rnd2, 1)
        }

    def name(self):
        return "The {name[1]} {name[2]}".format(name=self.names())


class WorldDestroyerNameGenerator2(BaseWorldDestroyerNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm4']),
            2: next(self.data['nm2']),  # nm2.splice(rnd2, 1)
        }

    def name(self):
        return "{name[2]} of {name[1]}".format(name=self.names())


class WorldDestroyerNameGenerator3(BaseWorldDestroyerNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm3']),  # nm3.splice(rnd, 1)
            2: next(self.data['nm2']),  # nm2.splice(rnd2, 1)
        }

    def name(self):
        return "The {name[1]} of {name[2]}".format(name=self.names())


class WorldDestroyerNameGenerator4(BaseWorldDestroyerNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm3']),  # nm3.splice(rnd, 1)
            2: next(self.data['nm2']),  # nm2.splice(rnd2, 1)
            3: next(self.data['nm1']),
        }

    def name(self):
        return "The {name[1]} {name[3]} {name[2]}".format(name=self.names())


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
