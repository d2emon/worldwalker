import random
from genelib.nested.item import NestedItem


class ChildrenGenerator:
    def __init__(self, item, amount=(1, None), probability=100):
        self.item = item
        self.amount = amount
        self.probability = probability

    def generate_amount(self):
        return random.randint(*self.amount) if self.amount[1] is not None else self.amount[0]

    def generate_probability(self):
        return random.randrange(100) < self.probability

    def generate(self):
        if not self.item:
            yield from []
        if not self.generate_probability():
            yield from []
        for _ in range(self.generate_amount()):
            yield NestedItem.get_item(self.item)

    def __add_group(self):
        if self.item[0] != '.':
            return [self]

        group = NestedItem.items[self.item[1:]]
        if group:
            return group.children

        return [self]

    @classmethod
    def parse(cls, data):
        def parse_amount(args):
            values = args.split('-')
            if len(values) < 2:
                return int(values[0]), None
            else:
                return int(values[0]), int(values[1])

        def parse_probability(args):
            values = (args + '?').split('%')
            if len(values) > 1:
                return int(values[0])
            else:
                return None

        if not isinstance(data, str):
            data = random.choice(data)
        data = data.split(',')

        child = cls(data[0])
        if len(data) >= 2:
            amount = parse_amount(data[1])
            probability = parse_probability(data[1])
            if probability is None:
                child.amount = 1, None
                child.probability = 100
            else:
                child.amount = amount
                child.probability = probability
        return child

    @classmethod
    def generate_child(cls, item, amount=(1,), probability=100):
        if random.randrange(1000) / 10 >= probability:
            yield from []
        for _ in range(*amount):
            yield item
