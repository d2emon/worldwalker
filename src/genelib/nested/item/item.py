import random


class NestedItem:
    class ItemGenerator:
        classes = []

        description_generator = None

        @classmethod
        def description(cls):
            return cls.description_generator

        @classmethod
        def children(cls):
            yield from []

        @classmethod
        def image(cls):
            while True:
                yield ''

        @classmethod
        def get_count(cls, count=(1, None), probability=100):
            if random.uniform(0, 100) >= probability:
                return 0
            elif count[1] is None:
                return count[0]
            else:
                return random.randint(*count)

        @classmethod
        def child(cls, class_name, count=(1, None), probability=100):
            for _ in range(cls.get_count(count, probability)):
                generator = next((c for c in cls.classes if c.__name__ == class_name), None)
                if generator is not None:
                    yield generator()

    item_type = None

    def __init__(self):
        self.__name = None
        self.__description = None
        self.__children = None
        self.__image = None
        self.parent = None

    @property
    def name(self):
        if self.__name is None:
            self.__name = self.item_type or self.__class__.__name__
        return self.__name

    @property
    def description(self):
        if self.__description is None:
            self.__description = next(self.ItemGenerator.description())
        return self.__description

    @property
    def children(self):
        if self.__children is None:
            self.__children = list(self.ItemGenerator.children())
        return self.__children

    @property
    def image(self):
        if self.__image is None:
            self.__image = next(self.ItemGenerator.image())
        return self.__image

    @classmethod
    def once(cls):
        yield cls()

    @classmethod
    def multiple(cls, min_count=1, max_count=None):
        if max_count is None:
            count = min_count
        else:
            count = random.randint(min_count, max_count)

        for _ in range(count):
            yield cls()

    @classmethod
    def probable(cls, probability=100):
        if random.uniform(0, 100) < probability:
            yield cls()
