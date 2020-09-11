from genelib.fng.named import Named
from ..database import GroupDataProvider
from games.worlds.genelib import ListNameGenerator


class ZombieNameGenerator(ListNameGenerator):
    default_provider = GroupDataProvider('zombie', 'nm1')


class Zombie(Named):
    """
    Zombies come in many shapes and sizes, many of which have their own nickname or type name. From bloaters and
    belchers to crawlers and runners, there's hundreds of different types of zombies both in fiction and in this
    generator, so there's plenty to pick from and plenty to fill your zombie world with.
    """
    name_generator = ZombieNameGenerator()
