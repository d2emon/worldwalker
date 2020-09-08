from ..services.items import ItemsService
from .base_item import BaseItemData


class ItemData(BaseItemData):
    def __init__(self, item_id):
        self.__object = ItemsService.get_item(item_id=item_id)

    @property
    def state(self):
        raise NotImplementedError()

    # Support
    @property
    def name(self):
        return self.__object.get("name", "")

    @property
    def descriptions(self):
        return self.__object.get("description", [])

    @property
    def max_state(self):
        return self.__object.get("max_state", 0)

    @property
    def flannel(self):
        return self.__object.get("flannel", True)

    @property
    def base_value(self):
        return self.__object.get("value", 0)

    def reload(self):
        pass
