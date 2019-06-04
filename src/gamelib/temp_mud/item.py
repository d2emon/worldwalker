from .player import Player
from .world import World


class Item:
    def __init__(self, item_id):
        self.item_id = item_id

    @classmethod
    def items(cls):
        return (Item(item_id) for item_id in range(World.item_ids))

    @property
    def __object(self):
        return World.objects[self.item_id]

    @property
    def __data(self):
        return World.objinfo[self.item_id]

    @property
    def name(self):
        return self.__object.name

    @property
    def max_state(self):
        return self.__object.max_state

    @property
    def flannel(self):
        return self.__object.flannel

    @property
    def base_value(self):
        return self.__object.value

    @property
    def location(self):
        return self.__data[0]

    def set_location(self, value, carry_flag):
        self.__data[0] = value
        self.carry_flag = carry_flag

    @property
    def carry_flag(self):
        return self.__data[3]

    @carry_flag.setter
    def carry_flag(self, value):
        self.__data[3] = value

    @property
    def is_destroyed(self):
        return self.test_bit(0)

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

    def create(self):
        self.clear_bit(0)

    def get_description(self, state):
        return self.__object.description[state]

    def set_bit(self, bit_id):
        self.__data[2] = bit_set(bit_id)

    def clear_bit(self, bit_id):
        self.__data[2] = bit_clear(bit_id)

    def test_bit(self, bit_id):
        return bit_fetch(self.__data[2], bit_id)

    def set_byte(self, byte_id, value):
        self.__data[2] = byte_put(byte_id, value)

    def get_byte(self, byte_id):
        return byte_fetch(self.__data[2], byte_id)

    def test_mask(self, mask):
        return all(self.test_bit(bit_id) for bit_id, value in enumerate(mask) if value)
