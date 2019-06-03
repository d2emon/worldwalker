from .player import Player


class Item:
    def __init__(self, item_id):
        self.item_id = item_id
        self.carry_flag = 0
        self.location = 0

    @property
    def is_light(self):
        if self.item_id == 32:
            return True
        if self.test_bit(13):
            return True
        return False

    @property
    def owner(self):
        if self.carry_flag in (0, 3):
            return None
        return Player(self.location)

    @classmethod
    def fobna(cls, item_name):
        raise NotImplementedError()

    def test_bit(self, bit_id):
        raise NotImplementedError()
