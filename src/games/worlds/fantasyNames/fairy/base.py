from games.worlds.database.provider import group_providers_from_list
from games.worlds.genelib import NameGenerator


class BaseFairyNameGenerator(NameGenerator):
    __DATABASE = 'fairy'
    __PARTS = [
        'namesMale',
        'namesFemale',
        'namesFamily',
        'namesFamily2',
    ]
    default_providers = group_providers_from_list(__DATABASE, __PARTS)
    used_parts = __PARTS
