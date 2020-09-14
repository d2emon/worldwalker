from .. import genders
from ..name import Name


class BaseNamedFactory:
    @property
    def factory(self):
        raise NotImplementedError()

    @property
    def gender(self):
        return genders.NEUTRAL

    def __iter__(self):
        return self

    def __next__(self):
        if self.factory is None:
            return None

        return Name(
            name=next(self.factory),
            gender=self.gender,
        )
