import random
from genelib.nested.item import NestedItem


class ChildrenGenerator:
    def __init__(self, thing, amount_min=1, amount_max=None, probability=100):
        self.thing = thing
        self.amount_min = amount_min
        self.amount_max = amount_max
        self.probability = probability

    def get_amount(self):
        if self.amount_max is None:
            return self.amount_min
        return random.randint(self.amount_min, self.amount_max)

    def get_probability(self):
        return random.randrange(100) < self.probability

    def generate(self):
        if not self.thing:
            return []
        if not self.get_probability():
            return []
        return [NestedItem.get_thing(self.thing) for _ in range(self.get_amount())]

    def add_group(self):
        if self.thing[0] != '.':
            return [self]

        group = NestedItem.things[self.thing[1:]]
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
            return None

        if not isinstance(data, str):
            data = random.choice(data)
        data = data.split(',')

        child = cls(data[0])
        if len(data) < 2:
            return child

        amount_min, amount_max = parse_amount(data[1])
        child.amount_min = amount_min
        child.amount_max = amount_max

        probability = parse_probability(data[1])
        if probability is None:
            child.amount_min = 1
            child.amount_max = None
            child.probability = 100
        else:
            child.probability = probability
        return child


class GeneratorsList:
    def __init__(self, generators):
        self.generators = generators

    def generate(self):
        return random.choice(self.generators).generate()


def parse_children_data(data):
    if isinstance(data, str):
        data = data,
    return GeneratorsList([ChildrenGenerator.parse(item) for item in data])


def generate_child(thing, amount=(1,), probability=100):
    if random.randrange(1000) / 10 >= probability:
        return []
    return [thing for _ in range(*amount)]
