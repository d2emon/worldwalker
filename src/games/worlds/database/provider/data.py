import random
from .base_data import BaseDataProvider


class DataProvider(BaseDataProvider):
    def __init__(self, values):
        super().__init__()
        self.data = values

    def by_value(self, value):
        return self.data[value] if self.item_class is not None else value

    def __next__(self):
        return random.choice(self.data)

    def ready(self):
        result = list(self.data)
        random.shuffle(result)
        return iter(result)
