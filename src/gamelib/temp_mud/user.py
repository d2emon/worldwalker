from .location import Location
from .player import Player


class User:
    wd_there = ""

    class NewUaf:
        my_lev = 0

    def __init__(self):
        self.has_farted = False
        self.player_id = 0
        self.__location_id = 0

    @property
    def is_wizard(self):
        return self.NewUaf.my_lev > 9

    @property
    def is_god(self):
        return self.NewUaf.my_lev > 9999

    @property
    def can_carry(self):
        max_items = self.max_items
        if max_items is None:
            return True
        items_count = sum(not item.is_destroyed and item.is_carried_by(self.player) for item in ITEMS)
        return items_count < max_items

    @property
    def is_dark(self):
        if self.is_wizard:
            return False
        if not self.location.is_dark:
            return False
        for item in filter(lambda i: i.is_light, ITEMS):
            if is_here(item):
                return False
            owner = item.owner
            if owner is not None and owner.location == self.__location_id:
                return False
        return True

    @property
    def location(self):
        return Location(self.__location_id)

    @property
    def max_items(self):
        if not self.player.is_wizard:
            return None
        if self.player.level < 0:
            return None
        return self.player.level + 5

    @property
    def player(self):
        return Player(self.player_id)

    def set_wd_there(self, zone, location_id):
        self.wd_there = zone + " " + location_id
