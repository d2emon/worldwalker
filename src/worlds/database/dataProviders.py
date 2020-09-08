import random
from .dataItems import LengthItem


class BaseDataProvider:
    item_class = None

    def by_value(self, value):
        if self.item_class is None:
            return value
        return self.item_class(value)

    def generate(self):
        raise NotImplementedError


class DataProvider(BaseDataProvider):
    def __init__(self, values):
        super().__init__()
        self.data = values

    def by_value(self, value):
        if self.item_class is None:
            return value
        return self.data[value]

    def ready(self):
        result = list(self.data)
        random.shuffle(result)
        return iter(result)

    def generate(self):
        return random.choice(self.data)


class NumberDataProvider(BaseDataProvider):
    def __init__(self, min_value, max_value, float_point=1):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        self.float_point = float_point

    def generate(self):
        return random.randrange(self.min_value, self.max_value) / self.float_point


class LengthProvider(NumberDataProvider):
    item_class = LengthItem

    def generate(self):
        return self.by_value(super().generate())
