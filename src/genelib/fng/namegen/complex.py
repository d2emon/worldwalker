import random


class ComplexFactory:
    class Cache:
        def __init__(self):
            self.__items = {}

        def get_item(self, key):
            return self.__items.get(key) or self.set_item(key)

        def set_item(self, key):
            self.__items[key] = key() if isinstance(key, type) else key
            return self.__items[key]

    def __init__(self, *args, **kwargs):
        self.__factory_id = None
        self.__cache = self.Cache()

        self.factories = {}
        self.factories.update({key: value for key, value in enumerate(args)})
        self.factories.update(kwargs)

    @property
    def factory_ids(self):
        return list(self.factories.keys())

    @property
    def factory_id(self):
        if self.__factory_id is None:
            self.__factory_id = random.choice(self.factory_ids)
        return self.__factory_id

    @factory_id.setter
    def factory_id(self, value):
        self.__factory_id = value

    @property
    def factory(self):
        return self.get(self.factory_id)

    def get(self, factory_id):
        return self.__cache.get_item(self.factories[factory_id])

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.factory) if len(self.factories) > 0 else None
