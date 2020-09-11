from ..provider.data import DataProvider
from ..item import DataItem


class ListDataProvider(DataProvider):
    item_class = DataItem

    def __init__(self, items):
        values = None
        if items is not None:
            values = [self.item_class(item_id, value) for item_id, value in enumerate(items)]
        super().__init__(values)
