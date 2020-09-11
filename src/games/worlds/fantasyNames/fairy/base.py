from genelib.fng.namegen import NameFactory
from games.worlds.database.provider import group_providers_from_list


class BaseNameFactory(NameFactory):
    __DATABASE = 'fairy'
    __PARTS = [
        'namesMale',
        'namesFemale',
        'namesFamily',
        'namesFamily2',
    ]
    default_providers = group_providers_from_list(__DATABASE, __PARTS)
    used_parts = __PARTS

    @property
    def names_male(self):
        return self.name_parts()['namesMale']

    @property
    def names_female(self):
        return self.name_parts()['namesFemale']

    @property
    def names_family(self):
        return self.name_parts()['namesFamily']

    @property
    def names_family_2(self):
        return self.name_parts()['namesFamily2']
