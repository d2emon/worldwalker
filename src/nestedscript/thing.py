import random


class Thing:
    thing_name = None
    name_generator = None

    def __init__(self):
        self.__name = None
        self.__children = None
        self.parent = None

    @property
    def name(self):
        if self.__name is None:
            self.__name = self.name_generator.generate()
        return self.__name

    @property
    def children(self):
        if self.__children is None:
            self.__children = sum(self.generate_children(), [])
        return self.__children

    @property
    def image(self):
        # special-case pictures
        if self.name == 'sharkverse':
            return "nestedSharkverse.png"
        elif self.name == 'baconverse':
            return "nestedBaconverse.png"
        elif self.name == 'doughnutverse':
            return "nestedDoughnutverse.png"
        elif self.name == 'lasagnaverse':
            return "nestedLasagnaverse.png"

    @classmethod
    def generate_children(cls):
        return []


class SizedThing(Thing):
    size_unit = 'm'

    def __init__(self, size=None):
        super().__init__()
        self.size = size or self.generate_size()

    @classmethod
    def generate_size(cls):
        return 1, 1, 1

    def generate_point(self):
        axles = [axle / 2 for axle in self.size]
        return [random.randint(-axle, axle) for axle in axles]


def generate_child(thing, amount=(1,), probability=100):
    if random.randrange(1000) / 10 >= probability:
        return []
    return [thing for _ in range(*amount)]