from .descr import DATA as DESCRIPTIONS
from .fantasyNames import FANTASY_NAMES_DATA
from .dataItems import DataItem, LengthItem
from .dataProviders import LengthProvider, DataProvider


DATA = {
    **FANTASY_NAMES_DATA,
    **DESCRIPTIONS,
}


class ListDataProvider(DataProvider):
    item_class = DataItem

    def __init__(self, items):
        values = None
        if items is not None:
            values = [self.item_class(item_id, value) for item_id, value in enumerate(items)]
        super().__init__(values)


def get_providers(items):
    return {item_id: ListDataProvider(values) for item_id, values in items.items()}


def get_providers_from_db(class_id):
    return get_providers(DATA[class_id])


def get_data(key, group_id):
    data = DATA.get(key)
    if not data:
        return None

    group = data.get(group_id)
    if not group:
        return None

    return group


class GroupDataProvider(ListDataProvider):
    def __init__(self, key, group_id):
        super().__init__(get_data(key, group_id))


def get_data_providers(key, items):
    return {item_id: GroupDataProvider(key, item_id) for item_id in items}


def get_syllable_providers(key, items):
    return {item_id: GroupDataProvider(key, item_key) for item_id, item_key in items.items()}
