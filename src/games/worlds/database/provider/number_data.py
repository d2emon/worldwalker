import random
from .base_data import BaseDataProvider


class NumberDataProvider(BaseDataProvider):
    def __init__(self, min_value, max_value, float_point=1):
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value
        self.float_point = float_point

    def __next__(self):
        return random.randrange(self.min_value, self.max_value) / self.float_point
