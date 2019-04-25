import random
from genelib import DataProvider
from .dataItems import DataItem, LengthItem


class BaseDataProvider:
    def generate(self):
        raise NotImplementedError


class NewDataProvider(BaseDataProvider):
    def __init__(self, values):
        super().__init__()
        self.data = [DataItem(item_id, value) for item_id, value in enumerate(values)]

    def generate(self):
        return random.choice(self.data)


class IntegerDataProvider(BaseDataProvider):
    def __init__(self, min_value, max_value):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

    def generate(self):
        return random.randrange(self.min_value, self.max_value)


class LengthProvider(IntegerDataProvider):
    def generate(self):
        return LengthItem(super().generate())
