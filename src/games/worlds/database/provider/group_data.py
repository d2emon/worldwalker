from db.fng import DATA
from .list_data import ListDataProvider


class GroupDataProvider(ListDataProvider):
    def __init__(self, key, group_id):
        super().__init__(self.get_data(key, group_id))

    @classmethod
    def get_data(cls, key, group_id):
        data = DATA.get(key)
        if not data:
            return None

        group = data.get(group_id)
        if not group:
            return None

        return group

    @classmethod
    def from_list(cls, key, items):
        return {values: cls(key, values) for item_id, values in enumerate(items)}

    @classmethod
    def from_dict(cls, key, items):
        return {item_id: cls(key, values) for item_id, values in items.items()}
