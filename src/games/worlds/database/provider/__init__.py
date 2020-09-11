from db.fng import DATA as __DATA

from .data import DataProvider
from .list_data import ListDataProvider
from .group_data import GroupDataProvider
from .number_data import NumberDataProvider
from .length import LengthProvider


def group_providers_from_list(key, items):
    return GroupDataProvider.from_list(key, items)


def group_providers_from_dict(key, items):
    return GroupDataProvider.from_dict(key, items)


def list_providers(text_generator_id):
    return {item_id: ListDataProvider(values) for item_id, values in __DATA[text_generator_id].items()}
