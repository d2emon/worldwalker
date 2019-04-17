from ..database import db_data_provider
from genelib import NameGenerator, Named


class BaseWorldDestroyerNameGenerator(NameGenerator):
    """
    World destroyers come in many different shapes and sizes, from a relatively small creature with (un)godly powers to
    massive, planet-sized beings who consume entire galaxies. This name generator is aimed at all of those and anything
    in between, though, to some extent, you could see the names in this generator as titles, rather than as names.
    You'll find results like 'Ruiner of Realms', 'The Grand Consumer' and 'Undoer of Life'.

    If you combine them you could end up with a long sequence of titles, similar to how royalty sometimes has multiple
    titles, but in a more gruesome way when it comes to world destroyers.
    """
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
        names = self.names()
        return "The {} {}".format(
            names[1],
            names[2],
        )


class WorldDestroyerNameGenerator2(BaseWorldDestroyerNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm4']),
            2: next(self.data['nm2']),  # nm2.splice(rnd2, 1)
        }

    def name(self):
        names = self.names()
        return "{} of {}".format(
            names[2],
            names[1],
        )


class WorldDestroyerNameGenerator3(BaseWorldDestroyerNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm3']),  # nm3.splice(rnd, 1)
            2: next(self.data['nm2']),  # nm2.splice(rnd2, 1)
        }

    def name(self):
        names = self.names()
        return "The {} {}".format(
            names[1],
            names[2],
        )


class WorldDestroyerNameGenerator4(BaseWorldDestroyerNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm3']),  # nm3.splice(rnd, 1)
            2: next(self.data['nm2']),  # nm2.splice(rnd2, 1)
            3: next(self.data['nm1']),
        }

    def name(self):
        names = self.names()
        return "The {} {} {}".format(
            names[1],
            names[3],
            names[2],
        )


class WorldDestroyer(Named):
    name_generators = [
        WorldDestroyerNameGenerator1(),
        WorldDestroyerNameGenerator1(),
        WorldDestroyerNameGenerator1(),
        WorldDestroyerNameGenerator2(),
        WorldDestroyerNameGenerator2(),
        WorldDestroyerNameGenerator2(),
        WorldDestroyerNameGenerator3(),
        WorldDestroyerNameGenerator3(),
        WorldDestroyerNameGenerator4(),
        WorldDestroyerNameGenerator4(),
        WorldDestroyerNameGenerator4(),
    ]
