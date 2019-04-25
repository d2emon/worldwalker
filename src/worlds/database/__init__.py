from .descr import DATA as DESCRIPTIONS
from .fantasyNames import FANTASY_NAMES_DATA
from .dataItems import DataItem, LengthItem
from .dataProviders import NewDataProvider, LengthProvider, DataProvider


DATA = {
    **FANTASY_NAMES_DATA,
    **DESCRIPTIONS,
}


def get_providers(class_id):
    providers_data = DATA[class_id]
    return {key: NewDataProvider(values) for key, values in providers_data.items()}


def get_data(key, group_id):
    data = DATA.get(key)
    if not data:
        return None

    group = data.get(group_id)
    if not group:
        return None

    return [DataItem(item_id, item) for item_id, item in enumerate(group)]


def db_data_provider(key, group_id):
    return DataProvider(get_data(key, group_id))


def get_data_providers(key, items):
    return {item: db_data_provider(key, item) for item in items}


def get_syllable_providers(key, items):
    return {item_id: db_data_provider(key, item_key) for item_id, item_key in items.items()}
