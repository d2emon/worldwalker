import random


class DataProvider:
    def __init__(self, data):
        self.data = data

    def ready(self):
        result = list(self.data)
        random.shuffle(result)
        return iter(result)
