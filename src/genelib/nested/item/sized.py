import random
from .item import NestedItem


class SizedItem(NestedItem):
    size_unit = 'm'

    class ItemGenerator(NestedItem.ItemGenerator):
        @classmethod
        def size(cls):
            return 1, 1, 1

    def __init__(self, size=None):
        super().__init__()
        self.__size = size

    @property
    def size(self):
        if self.__size is None:
            self.__size = self.ItemGenerator.size()
        return self.__size

    def get_point(self):
        axles = [int(x / 2) for x in self.size]
        return [random.randint(-x, x) for x in axles]
