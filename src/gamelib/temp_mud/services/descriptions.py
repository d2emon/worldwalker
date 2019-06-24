from ..errors import ServiceError
from ..item.item import Item


class DescriptionService:
    __descriptions = {}
    __default = "You see nothing special.\n"

    @classmethod
    def get(cls, **kwargs):
        item_id = kwargs.get('item_id')
        # self.connect(EXAMINES + item_id, "r")
        return cls.__descriptions.get(item_id, default=cls.__default)
