from genelib.fng.namegen import NameFactory
from games.worlds.database.provider import group_providers_from_list


DATABASE = 'witch'
PARTS = [
    'nm1',
    'nm2',
    'nm3',
]


class BaseNameFactory(NameFactory):
    default_providers = group_providers_from_list(DATABASE, PARTS)
    used_parts = PARTS

    @property
    def nm1(self):
        return self.name_parts()['nm1']

    @property
    def nm2(self):
        return self.name_parts()['nm2']

    @property
    def nm3(self):
        return self.name_parts()['nm3']
