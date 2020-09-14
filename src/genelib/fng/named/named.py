from .. import genders


class Named:
    name_factory = None

    def __init__(self, name='', *args, **kwargs):
        self.name = str(name)

    @property
    def title(self):
        return self.name.title()

    def __str__(self):
        return self.title

    @classmethod
    def factory(cls, *args, **kwargs):
        name = cls.name_factory.next(*args, **kwargs)
        return cls(
            name=name.name if name else '',
            gender=name.gender if name else genders.NEUTRAL,
        )
