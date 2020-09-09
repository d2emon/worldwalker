import random
from .children_generator import ChildrenGenerator


class GeneratorsList:
    def __init__(self, generators):
        self.generators = generators

    def __next__(self):
        return next(random.choice(self.generators))

    @classmethod
    def parse_children_data(cls, data):
        data = [data] if isinstance(data, str) else data
        data = [ChildrenGenerator.parse(i) for i in data]
        return cls(data)
