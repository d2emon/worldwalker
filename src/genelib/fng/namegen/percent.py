import random
from .complex import ComplexFactory


class PercentsFactory(ComplexFactory):
    def __init__(self, percents=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__factory_id = None
        if percents is not None:
            self.factories.update({percent: factory for percent, factory in percents.items()})

    @property
    def factory_ids(self):
        return sorted(self.factories.keys())

    @property
    def factory_id(self):
        if self.__factory_id is None:
            self.__factory_id = random.uniform(0, 100)
        return self.__factory_id

    @factory_id.setter
    def factory_id(self, value):
        self.__factory_id = value

    @property
    def factory(self):
        for factory_id in self.factory_ids:
            if factory_id >= self.factory_id:
                return self.get(factory_id)
        return None
