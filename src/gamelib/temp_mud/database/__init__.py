from itertools import chain


class DataFilter:
    def __init__(self, items=None):
        self.__items = items or []

    def filter(self, **kwargs):
        return ItemsData(filter(self.__filter(**kwargs), self.__items))

    def or_filter(self, *items):
        return ItemsData(chain(self.__items, *items))

    @classmethod
    def __filter(cls, **kwargs):
        return lambda item: all(f(item) for f in cls.__filters(**kwargs))

    @classmethod
    def __filters(cls, **kwargs):
        raise NotImplementedError()

    @property
    def first(self):
        return next(self.__items, None)

    @property
    def count(self):
        return any(self.__items)

    @property
    def all(self):
        return list(self.__items)


class ItemsData(DataFilter):
    @classmethod
    def __filters(
        cls,
        carried_in=None,
        destroyed=None,
        is_light=None,
        item=None,
        location=None,
        mask=None,
        not_worn_by=None,
        owner=None,
        **kwargs
    ):
        if carried_in is not None:
            yield lambda i: i.owner and carried_in.equal(i.owner.location)
        if destroyed is not None:
            yield lambda i: i.is_destroyed == destroyed
        if is_light is not None:
            yield lambda i: i.is_light == is_light
        if item is not None:
            yield lambda i: i == item
        if location is not None:
            yield lambda i: i.location and location.equal(i.location)
        if mask is not None:
            yield lambda i: i.test_mask(mask)
        if not_worn_by is not None:
            yield lambda i: not i.is_worn_by(not_worn_by)
        if owner is not None:
            yield lambda i: owner.equal(i.owner)

    def not_destroyed(self, user):
        return self if user.is_wizard else self.filter(destroyed=False)


class PlayerData(DataFilter):
    @classmethod
    def __filters(
        cls,
        name=None,
        player=None,
        visible=None,
        location=None,
        **kwargs
    ):
        if name is not None:
            # Player.find(name)
            yield lambda i: i.name == name
        if player is not None:
            yield lambda i: player.equal(i)
        if visible is not None:
            yield lambda i: i.visible <= visible
        if location is not None:
            yield lambda i: location.equal(i.location)


class LocationData(DataFilter):
    @classmethod
    def __filters(
        cls,
        location_id=None,
        **kwargs
    ):
        if id is not None:
            # location(location_id)
            yield lambda i: i.location_id == location_id
