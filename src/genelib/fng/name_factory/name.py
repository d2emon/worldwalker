from ..namegen import ComplexFactory


class NameFactory:
    factory = ComplexFactory()

    @classmethod
    def next(cls, *args, **kwargs):
        cls.factory.factory_id = None
        return next(cls.factory)
