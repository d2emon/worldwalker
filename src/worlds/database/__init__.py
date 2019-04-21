from genelib import DataProvider
from .fantasyNames import FANTASY_NAMES_DATA


class DataItem:
    def __init__(self, item_id, text):
        self.item_id = item_id
        self.__text = text

    def __str__(self):
        return self.__text


def get_data(key, group_id):
    data = FANTASY_NAMES_DATA.get(key)
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
