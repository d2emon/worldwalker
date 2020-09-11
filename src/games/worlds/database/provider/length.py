from .number_data import NumberDataProvider
from ..item import LengthItem


class LengthProvider(NumberDataProvider):
    item_class = LengthItem

    def __next__(self):
        return self.by_value(super().__next__())
