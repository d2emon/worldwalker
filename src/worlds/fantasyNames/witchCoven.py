from ..database import get_data_providers
from genelib import NameGenerator, Named, build_name_generator


class BaseWitchCovenNameGenerator(NameGenerator):
    default_providers = get_data_providers('witch-coven', [
        'nm1',
        'nm2',
        'nm3',
    ])


class WitchCovenNameGenerator1(BaseWitchCovenNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm1']),  # nm1.splice(rnd, 1)
            2: next(self.data['nm3']),
        }

    def name(self):
        return "The {name[1]} {name[2]}".format(name=self.names())


class WitchCovenNameGenerator2(BaseWitchCovenNameGenerator):
    def names(self):
        return {
            1: next(self.data['nm2']),  # nm2.splice(rnd, 1)
            2: next(self.data['nm3']),
        }

    def name(self):
        return "{name[2]} of {name[1]}".format(name=self.names())


class WitchCoven(Named):
    """
    A coven is a group of witches, which can come in different forms depending on the type of witchcraft the witches
    belong to. The coven might be a community of many, a mere handful or anything in between. It could be a permanent
    group or merely a temporary gathering and so on.

    Coven names can also vary greatly, although I did notice several themes in existing coven names and I used these
    themes for the names in this generator. A coven's name is usually a very personal choice however, but hopefully
    this name generator will be helpful nonetheless.
    """
    name_generator = build_name_generator(
        (WitchCovenNameGenerator1, 0, 5),
        (WitchCovenNameGenerator2, 5, 10),
    )
