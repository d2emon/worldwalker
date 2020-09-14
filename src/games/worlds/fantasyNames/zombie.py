from genelib.fng.name_factory import NameFactory as BaseNameFactory
from ..database import GroupDataProvider
from games.worlds.genelib import ListNameGenerator


class ZombieNameGenerator(ListNameGenerator):
    def __init__(self, providers=None):
        super().__init__(providers or GroupDataProvider('zombie', 'nm1'))


class NameFactory(BaseNameFactory):
    factory = ZombieNameGenerator()
