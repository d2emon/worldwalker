from genelib.fng.namegen import NameFactory
from games.worlds.database.provider import group_providers_from_list


class BaseNameFactory(NameFactory):
    DATABASE = 'witch-coven'
    PARTS = [
        'nm1',  # nm1.splice(rnd, 1)
        'nm2',  # nm2.splice(rnd, 1)
        'nm3',
    ]

    NAME_V1 = 1
    NAME_V2 = 2
    name_type = NAME_V1
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


class NameFactory1(BaseNameFactory):
    name_type = BaseNameFactory.NAME_V1

    @property
    def name(self):
        return f'The {self.nm1} {self.nm3}'


class NameFactory2(BaseNameFactory):
    name_type = BaseNameFactory.NAME_V2

    @property
    def name(self):
        return f'{self.nm3} of {self.nm2}'
