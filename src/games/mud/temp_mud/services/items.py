from ..errors import ServiceError
from .data.items import ITEMS
from .descriptions import DescriptionService
from .world import WorldService


class ItemsService:
    __OBMUL = 8

    __items_count = 196
    __items = ITEMS

    @classmethod
    def __get_item_id(cls, **kwargs):
        item_id = kwargs.get('item_id')
        if not 0 <= item_id < cls.__items_count:
            raise ServiceError("No item with this item id")
        return item_id

    @classmethod
    def get_description(cls, **kwargs):
        item_id = cls.__get_item_id(**kwargs)
        return DescriptionService.get(item_id=item_id)

    @classmethod
    def get_info(cls, **kwargs):
        item_id = cls.__get_item_id(**kwargs)
        return WorldService.get_item(item_id=item_id)

    @classmethod
    def get_item(cls, **kwargs):
        item = cls.__items[cls.__get_item_id(**kwargs)]
        return {
            "name": item[0],
            "description": item[1],
            "max_state": item[2],
            "flannel": item[3],
            "value": item[4],
        }

    @classmethod
    def get_items_count(cls):
        return cls.__items_count
