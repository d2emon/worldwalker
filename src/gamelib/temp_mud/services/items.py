from .descriptions import DescriptionService
from .world import WorldService


class ItemsService:
    __OBMUL = 8
    __NOBS = 196

    __objects = []

    @classmethod
    def get_description(cls, **kwargs):
        item_id = kwargs.get('item_id')
        return DescriptionService.get(item_id=item_id)

    @classmethod
    def get_info(cls, **kwargs):
        item_id = kwargs.get('item_id')
        return WorldService.get_item(item_id=item_id)

    @classmethod
    def get_item(cls, **kwargs):
        item_id = kwargs.get('item_id')
        return cls.__objects[item_id]
