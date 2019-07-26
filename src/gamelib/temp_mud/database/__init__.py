from itertools import chain


class DataFilter:
    def __init__(self, items=None):
        self.items = items or []

    def filter(self, **kwargs):
        return ItemsData(filter(self.__filter(**kwargs), self.items))

    def or_filter(self, *items):
        return ItemsData(chain(self.items, *items))

    @classmethod
    def __filter(cls, **kwargs):
        return lambda item: all(f(item) for f in cls.__filters(**kwargs))

    @classmethod
    def __filters(cls, **kwargs):
        raise NotImplementedError()

    @property
    def first(self):
        return next(list(self.items), None)


class ItemsData(DataFilter):
    @classmethod
    def __filters(
        cls,
        carried_by=None,
        carried_in=None,
        is_destroyed=None,
        is_light=None,
        item=None,
        location=None,
        mask=None,
        owner=None,
        user=None,
        **kwargs
    ):
        if carried_by is not None:
            yield lambda i: i.is_carried_by(carried_by)
        if carried_in is not None:
            yield lambda i: i.owner and carried_in.equal(i.owner.location)
        if is_destroyed is not None:
            yield lambda i: i.is_destroyed == is_destroyed
        if is_light is not None:
            yield lambda i: i.is_light == is_light
        if item is not None:
            yield lambda i: i == item
        if location is not None:
            yield lambda i: i.is_in_location(location)
        if mask is not None:
            yield lambda i: i.test_mask(mask)
        if owner is not None:
            yield lambda i: owner.equal(i.owner)
        if user is not None and not user.is_wizard:
            yield from cls.__filters(is_destroyed=False)


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
