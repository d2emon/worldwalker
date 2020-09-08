import random


class NestedItem:
    class ItemGenerator:
        default_name = None
        name_generator = None

        @classmethod
        def name(cls):
            return cls.name_generator.generate()

        @classmethod
        def children(cls):
            return []

        @classmethod
        def image(cls):
            return ''

        @classmethod
        def child(cls, generator, amount=(1,), probability=100):
            if random.randrange(1000) / 10 >= probability:
                yield from []
                return

            for _ in range(*amount):
                yield generator

    def __init__(self):
        self.__name = None
        self.__children = None
        self.__image = None
        self.parent = None

    @property
    def name(self):
        if self.__name is None:
            self.__name = self.ItemGenerator.name()
        return self.__name

    @property
    def children(self):
        if self.__children is None:
            self.__children = self.ItemGenerator.children()
        return self.__children

    @property
    def image(self):
        if self.__image is None:
            self.__image = self.ItemGenerator.image()
        return self.__image
