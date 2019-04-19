from ..database import get_data_providers
from genelib import NameGenerator, Named, build_name_generator


class BaseWorldDefenderNameGenerator(NameGenerator):
    default_providers = get_data_providers('world-defender', [
        'nm1',
        'nm2',
        'nm3',
        'nm4',
    ])


class WorldDefenderNameGenerator1(BaseWorldDefenderNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm1']),
            2: next(self.data['nm2']),  # nm2.splice(rnd2, 1)
        }

    def name(self):
        return "The {name[1]} {name[2]}".format(name=self.names())


class WorldDefenderNameGenerator2(BaseWorldDefenderNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm4']),
            2: next(self.data['nm2']),  # nm2.splice(rnd2, 1)
        }

    def name(self):
        return "{name[2]} of {name[1]}".format(name=self.names())


class WorldDefenderNameGenerator3(BaseWorldDefenderNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm3']),  # nm3.splice(rnd, 1)
            2: next(self.data['nm2']),  # nm2.splice(rnd2, 1)
        }

    def name(self):
        return "The {name[1]} of {name[2]}".format(name=self.names())


class WorldDefenderNameGenerator4(BaseWorldDefenderNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm3']),  # nm3.splice(rnd, 1)
            2: next(self.data['nm2']),  # nm2.splice(rnd2, 1)
            3: next(self.data['nm1']),
        }

    def name(self):
        return "The {name[1]} {name[3]} {name[2]}".format(name=self.names())


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
