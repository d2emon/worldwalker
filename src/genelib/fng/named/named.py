from ..namegen import ComplexFactory


class Named:
    class NameFactory:
        factory = ComplexFactory()

        @classmethod
        def next(cls, *args, **kwargs):
            cls.factory.factory_id = None
            return next(cls.factory)

    def __init__(self, name='', *args, **kwargs):
        self.name = str(name)

    @property
    def title(self):
        return self.name.title()

    def __str__(self):
        return self.title

    @classmethod
    def generate(cls, *args, **kwargs):
        return cls(cls.NameFactory.next(*args, **kwargs), *args, **kwargs)
